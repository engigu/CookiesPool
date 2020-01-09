




var vue = new Vue({
    el: "#site",
    data () {
        return {
            "col_list": ["No", "Cookies", "ModifiedAt","Status"],
            "list_data": "",
            "total": ""
        }
    },
    mounted () {
        axios.get('/cookies_all').then(response => (
            this.list_data = response.data.cookies,
            this.total = response.data.total
            )).catch(function (err) {
            console.log(err)
        })
    }
})

