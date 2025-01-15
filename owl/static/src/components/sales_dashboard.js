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
        this.chartOrderExpenseRef = useRef("chart_order_per_expense")
        this.chartDailyProfitRef = useRef("chart_daily_profit")
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
            period: 30,
            store: "tous",
            data_order_expense: {
                labels:[],
                datasets:[]
              },
              data_daily_profit: {
                labels:[],
                datasets:[]
              }
        })
        this.orm = useService('orm')
        this.actionService = useService("action")

        onWillStart(async () => {
            await loadJS("/owl/static/src/lib/chart.umd.min.js")
            this.getDates()
            await this.getOrders()
            await this.getDataOrderExpense()
            await this.getDataDailyProfit()
        })

        onMounted(() => this.renderChart())
    }

    getMonthsName() {
        const months = [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ];
    
        const today = new Date();
        const currentMonthIndex = today.getMonth();
    
        // Calculer les indices des mois
        const previousMonthIndex1 = (currentMonthIndex - 1 + 12) % 12;
        const previousMonthIndex2 = (currentMonthIndex - 2 + 12) % 12;
    
        // Retourner les noms des mois
        return [
            months[currentMonthIndex],         // Mois courant
            months[previousMonthIndex1],      // Mois précédent
            months[previousMonthIndex2],      // Mois d'avant
        ];
    }

    getDayName() {
        const today = new Date();
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    
        let dates = [];
        let currentDate = new Date(startOfMonth);
    
        while (currentDate <= today) {
            dates.push(currentDate.toISOString().split("T")[0]); // Formate en "YYYY-MM-DD"
            currentDate.setDate(currentDate.getDate() + 1); // Passe au jour suivant
        }
    
        return dates;
      }
    

    async getDataDailyProfit() {
        const labels =  this.getDayName()
        this.state.data_daily_profit.labels = labels

        // data
        // const 
        
        // const current_revenues = await this.orm.readGroup('sale.order', domain, ["amount_total:sum"], [''])
        let profits = []
        let i=10
        console.log("labels", labels)
        labels.forEach(async (label) => {
          let start = label+ " 00:00:00"
          let end = label+ " 23:59:59"
          let domain = [['state', 'in', ['sale']],['date_entry', '>=', start],['date_entry', '<=', end]]
          let edomain = [['state', 'in', ['done']],['date', '>=', start],['date', '<=', end]]

          const amount_order = await this.orm.readGroup('sale.order', domain, ["amount_total:sum"], [])
          const amount_expense = await this.orm.readGroup('hr.expense', edomain, ["total_amount_currency:sum"], [])
          const total_order = amount_order[0].amount_total ? amount_order[0].amount_total : 0
          const total_expense = amount_expense[0].total_amount_currency ? amount_expense[0].total_amount_currency : 0
          profits.push(total_order - total_expense)
          console.log("profits", profits)
        })
        
        const datasets = [
          {
            label: 'Evolution bénéfice par jour',
            data: profits,
            hoverOffset: 4
          }
        ]

        this.state.data_daily_profit.datasets = datasets
    }

    async getDataOrderExpense() {
        const labels =  this.getMonthsName()
        this.state.data_order_expense.labels = labels.reverse()


        // data
        const domain = [['state', 'in', ['sale']],['date_entry', '>=', this.state.date]]
        const prev_domain = [['state', 'in', ['sale']],['date_entry', '>=', this.state.previous_date], ['date_entry', '<',this.state.date]]
        const prev_prev_domain = [['state', 'in', ['sale']],['date_entry', '>=', this.state.previous_previous_date], ['date_entry', '<',this.state.previous_date]]
        
        const current_revenues = await this.orm.readGroup('sale.order', domain, ["amount_total:sum"], [])
        const prev_revenues = await this.orm.readGroup('sale.order', prev_domain, ["amount_total:sum"], [])
        const prev_prev_revenues = await this.orm.readGroup('sale.order', prev_prev_domain, ["amount_total:sum"], [])

        
        const revenues = [ prev_prev_revenues[0].amount_total, prev_revenues[0].amount_total, current_revenues[0].amount_total]
        
        // expence
        const edomain = [['state', 'in', ['done']],['date', '>=', this.state.date]]
        const eprev_domain = [['state', 'in', ['done']],['date', '>=', this.state.previous_date], ['date', '<',this.state.date]]
        const eprev_prev_domain = [['state', 'in', ['done']],['date', '>=', this.state.previous_previous_date], ['date', '<',this.state.previous_date]]
        
        const current_expenses = await this.orm.readGroup('hr.expense', edomain, ["total_amount_currency:sum"], [])
        const prev_expenses = await this.orm.readGroup('hr.expense', eprev_domain, ["total_amount_currency:sum"], [])
        const prev_prev_expenses = await this.orm.readGroup('hr.expense', eprev_prev_domain, ["total_amount_currency:sum"], [])

        const expenses = [ prev_prev_expenses[0].total_amount_currency, prev_expenses[0].total_amount_currency, current_expenses[0].total_amount_currency]

        const datasets = [
          {
            label: 'Total ventes du mois',
            data: revenues,
            backgroundColor:['blue', 'blue', 'blue'],
            hoverOffset: 4
          },{
            label: 'Total dépenses du mois',
            data: expenses,
            backgroundColor:['red', 'red', 'red'],
            hoverOffset: 4
          }
        ]

        this.state.data_order_expense.datasets = datasets
    }

 

    renderChart() {
        

        new Chart(
            this.chartOrderExpenseRef.el,
            {
              type: "bar",
              data: {
                labels: this.state.data_order_expense.labels,
                datasets: this.state.data_order_expense.datasets
              },
              options: {
                responsive: true, 
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display:true,
                        text:'Commandes et Dépenses',
                        position:'bottom'
                    }
                }
              }
            }
          );


          new Chart(
            this.chartDailyProfitRef.el,
            {
              type: "line",
              data: {
                labels: this.state.data_daily_profit.labels,
                datasets: this.state.data_daily_profit.datasets
              },
              options: {
                responsive: true, 
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display:true,
                        text:'Evolution bénéfice par jour',
                        position:'bottom'
                    }
                }
              }
            }
          );
    }

    async onChangeStore() {
        console.log(this.state.store)
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

        // previous previous date
        const startOfTwoMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 2, 1);
        let formatedPreviousPreviousDate = this.formatDate(startOfTwoMonthsAgo)
        this.state.previous_previous_date = formatedPreviousPreviousDate
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

    
   
    
}

OwlSalesDashboard.template = "owl.OwlSalesDashboard"
OwlSalesDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add('owl.sales_dashboard', OwlSalesDashboard)