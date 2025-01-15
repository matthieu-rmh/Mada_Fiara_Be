/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"
import { session } from "@web/session"
const { Component, onWillStart, useRef, onMounted, useState } = owl

export class OwlSalesDashboard extends Component {
    setup() {
        this.state = useState({
            orders: {
                 value:0,
                 percentage:0
            },
            visits: {
                value:0,
                percentage:0
            },
            ratio_orders_visits: {
                value:0,
                percentage:0
            },
            amount_to_be_done: {
                value:0,
                percentage:0
            },
            visits_of_the_day: [],
            day_remain:0,
            period: 30
        })
        this.orm = useService('orm')
        this.actionService = useService("action")

        onWillStart(async () => {
            this.getDates()
            await this.getOrders()
            await this.getVisits()
            await this.getRatioOrdersVisits()
            await this.getAmountToBeDone()
            await this.getDayRemain()
            await this.getVisitsOfTheDay()
        })
    }

    async onChangePeriod() {
        this.getDates()
        await this.getOrders()
        await this.getVisits()
        await this.getRatioOrdersVisits()
        await this.getAmountToBeDone()
    }

    getDates () {
        let today = new Date();
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1); 
        let formatedDate = this.formatDate(startOfMonth)
        this.state.date = formatedDate

        // previous date
        const startOfLastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
        let formatedPreviousDate = this.formatDate(startOfLastMonth)
        this.state.previous_date = formatedPreviousDate
    }

    getTodayStart() {
        const today = new Date();
        const year = today.getFullYear();
        const month = (today.getMonth() + 1).toString().padStart(2, '0'); // Mois en base 1
        const day = today.getDate().toString().padStart(2, '0');

        const formattedDate = `${year}-${month}-${day} 00:00:00`;

        return formattedDate
    }

    getTodayEnd() {
        const today = new Date();
        const year = today.getFullYear();
        const month = (today.getMonth() + 1).toString().padStart(2, '0'); // Mois en base 1
        const day = today.getDate().toString().padStart(2, '0');

        const formattedDate = `${year}-${month}-${day} 23:59:59`;

        return formattedDate
    }

    async viewPartnerVisits(id){
        let domain = [['id', '=', id]]
        

        // let list_view = await this.orm.searchRead("ir.model.data", [['name', '=', 'view_partner_form']])

        


        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Partner",
            res_model: "res.partner",
            res_id:1050,
            domain,
            // context: {group_by: ['date_order']},
            views: [
                [false, "list"],
                [false, "form"],
            ]
        })
    }

    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Mois (01-12)
        const day = String(date.getDate()).padStart(2, '0'); // Jour (01-31)
        const hours = String(date.getHours()).padStart(2, '0'); // Heures (00-23)
        const minutes = String(date.getMinutes()).padStart(2, '0'); // Minutes (00-59)
        const seconds = String(date.getSeconds()).padStart(2, '0'); // Secondes (00-59)
    
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }

    formatNumber(value) {
        if (value >= 1e6) {
            return (value / 1e6).toFixed(2) + 'M'; // Millions
        } else if (value >= 1e3) {
            return (value / 1e3).toFixed(2) + 'K'; // Milliers
        } else {
            return value.toString(); // Si inférieur à 1000
        }
    }

    async getVisitsOfTheDay() {
        let domain = [['user_id', '=', session.uid], ['start', '>=', this.getTodayStart()], ['stop', '<=', this.getTodayEnd()]]
    
        const data = await this.orm.searchRead('calendar.event', domain)
        console.log("data", data)
        this.state.visits_of_the_day = data
    }

    async getAmountToBeDone() {
        const domain = [['user_id', '=', session.uid],['state', 'in', ['sale']],['date_order', '>=', this.state.date]]
        
        const current_revenues = await this.orm.readGroup('sale.order', domain, ["amount_total:sum"], [])
        const user_target = await this.orm.readGroup('res.users', [['id', '=', session.uid]], ["customer_amount_target:sum"], [])
        const amount_target = user_target[0].customer_amount_target ? user_target[0].customer_amount_target : 0
        const amount_revenues = current_revenues[0].amount_total ? current_revenues[0].amount_total : 0
        this.state.amount_to_be_done.value = this.formatNumber(amount_target - amount_revenues)
    }

    getDayRemain() {
        const today = new Date(); // Date actuelle
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();

        // Trouver le dernier jour du mois courant
        const lastDayOfMonth = new Date(currentYear, currentMonth + 1, 0);

        let workingDays = 0;
        let currentDate = new Date(today);

        // Parcourir les jours restants du mois
        while (currentDate <= lastDayOfMonth) {
            const dayOfWeek = currentDate.getDay();
            // Compter les jours si ce n'est ni un samedi (6) ni un dimanche (0)
            if (dayOfWeek !== 0 && dayOfWeek !== 6) {
                workingDays++;
            }
            // Passer au jour suivant
            currentDate.setDate(currentDate.getDate() + 1);
        }

        

        this.state.day_remain = workingDays 
    }

    async getOrders() {
        let domain = [['user_id', '=', session.uid],['state', 'in', ['sale']]]
        if(this.state.period > 0) {
            domain.push(['date_order', '>=', this.state.date])
        }
        const data = await this.orm.searchCount('sale.order', domain)
        this.state.orders.value = data

        // previous period
        let prev_domain = [['user_id', '=', session.uid],['state', 'in', ['sale']]]
        if(this.state.period > 0) {
            prev_domain.push(['date_order', '>=', this.state.previous_date], ['date_order', '<',this.state.date])
        }
        const prev_data = await this.orm.searchCount('sale.order', prev_domain)
        const percentage = prev_data != 0 ?((data - prev_data)/prev_data) * 100 : 0
        this.state.orders.percentage = percentage.toFixed(2)
            
    }

    async getVisits() {
        let domain = [['user_id', '=', session.uid]]
        if(this.state.period > 0) {
            domain.push(['start', '>=', this.state.date])
        }
        const data = await this.orm.searchCount('calendar.event', domain)
        this.state.visits.value = data

        // previous period
        let prev_domain = [['user_id', '=', session.uid]]
        if(this.state.period > 0) {
            prev_domain.push(['start', '>=', this.state.previous_date], ['start', '<',this.state.date])
        }
        const prev_data = await this.orm.searchCount('calendar.event', prev_domain)
        const percentage = prev_data != 0 ?((data - prev_data)/prev_data) * 100 : 0
        this.state.visits.percentage = percentage.toFixed(2)
            
    }
    async getRatioOrdersVisits() {
        // orders
        let _domain = [['user_id', '=', session.uid],['state', 'in', ['sale']]]
        if(this.state.period > 0) {
            _domain.push(['date_order', '>=', this.state.date])
        }
        const order_data = await this.orm.searchCount('sale.order', _domain)

        // previous period
        let _prev_domain = [['user_id', '=', session.uid],['state', 'in', ['sale']]]
        if(this.state.period > 0) {
            _prev_domain.push(['date_order', '>=', this.state.previous_date], ['date_order', '<',this.state.date])
        }
        const prev_order_data = await this.orm.searchCount('sale.order', _prev_domain)



        // visit
        let domain = [['user_id', '=', session.uid],]
        if(this.state.period > 0) {
            domain.push(['start', '>=', this.state.date])
        }
        const visit_data = await this.orm.searchCount('calendar.event', domain)

        // previous visit
        let prev_domain = [['user_id', '=', session.uid]]
        if(this.state.period > 0) {
            prev_domain.push(['start', '>=', this.state.previous_date], ['start', '<',this.state.date])
        }
        const prev_visit_data = await this.orm.searchCount('calendar.event', prev_domain)
        
        // ratio order visit
        const ratio_order_visit = visit_data != 0 ?(order_data/visit_data) * 100 : 0
        this.state.ratio_orders_visits.value = ratio_order_visit + "%"

        // previous ratio order visit
        const prev_ratio_order_visit = prev_visit_data != 0 ?(prev_order_data/prev_visit_data) * 100 : 0
        const percentage = prev_ratio_order_visit != 0 ?((ratio_order_visit - prev_ratio_order_visit)/prev_ratio_order_visit) * 100 : 0
        this.state.ratio_orders_visits.percentage = percentage.toFixed(2)
    }
    
}

OwlSalesDashboard.template = "owl.OwlSalesDashboard"
OwlSalesDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add('owl.sales_dashboard', OwlSalesDashboard)