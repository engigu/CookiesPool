
var site = new Vue({
    el: "#site",
    data () {
        return {
            "col_list": ["No", "Cookies", "ModifiedAt","Status"],
            "list_data": "",
            "total": ""
        }
    },
    // mounted () {
    //     axios.get('/cookies_all?site=58').then(response => (
    //         this.list_data = response.data.cookies,
    //         this.total = response.data.total
    //         )).catch(function (err) {
    //         console.log(err)
    //     })
    // }
})


var sites = new Vue({
    el: "#site_block",
    data () {
        return {
            "sites": "",
            "total": ""
        }
    },
    mounted () {
        axios.get('/cookies_all_sites').then(response => (
            this.sites = response.data.sites,
            this.total = response.data.total
            )).catch(function (err) {
            console.log(err)
        })
    }
})
