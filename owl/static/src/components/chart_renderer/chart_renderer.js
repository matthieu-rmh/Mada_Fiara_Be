/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"
import { session } from "@web/session"
const { Component, onWillStart, useRef, onMounted, useState } = owl

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart")
        this.state = useState({
          data: {
            labels:[],
            datasets:[]
          },
          period: 30,
          store:"tous"
        })
        this.orm = useService('orm')

        onWillStart(async ()=> {
            
            // await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js")
            await loadJS("/owl/static/src/lib/chart.umd.min.js")
            this.getDates()
            await this.getData()
        })

        onMounted(() => this.renderChart())
    }

    onChangeStore() {
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

    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Mois (01-12)
      const day = String(date.getDate()).padStart(2, '0'); // Jour (01-31)
      const hours = String(date.getHours()).padStart(2, '0'); // Heures (00-23)
      const minutes = String(date.getMinutes()).padStart(2, '0'); // Minutes (00-59)
      const seconds = String(date.getSeconds()).padStart(2, '0'); // Secondes (00-59)
  
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
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

    async getData() {
      if(this.props.name == 'order_per_expence') {
        const labels =  this.getMonthsName()
        this.state.data.labels = labels.reverse()

        console.log("this.props.store", this.props.store)

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

        this.state.data.datasets = datasets

      }else if(this.props.name == 'daily_profit') {
        const labels =  this.getDayName()
        this.state.data.labels = labels

        // data
        // const 
        
        // const current_revenues = await this.orm.readGroup('sale.order', domain, ["amount_total:sum"], [''])
        let profits = []
        let i=10
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
        })
        
        const datasets = [
          {
            label: 'Evolution bénéfice par jour',
            data: profits,
            hoverOffset: 4
          }
        ]

        this.state.data.datasets = datasets
      }
    }

    renderChart() {
        // const data = [
        //     { year: 2010, count: 10 },
        //     { year: 2011, count: 20 },
        //     { year: 2012, count: 15 },
        //     { year: 2013, count: 25 },
        //     { year: 2014, count: 22 },
        //     { year: 2015, count: 30 },
        //     { year: 2016, count: 28 },
        //   ];data.map(row => row.count)

        new Chart(
            this.chartRef.el,
            {
              type: this.props.type,
              data: {
                labels: this.state.data.labels,
                datasets: this.state.data.datasets
              },
              options: {
                responsive: true, 
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display:true,
                        text:this.props.title,
                        position:'bottom'
                    }
                }
              }
            }
          );
    }
}

ChartRenderer.template = "owl.ChartRenderer"
