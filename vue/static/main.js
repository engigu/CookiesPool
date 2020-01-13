
function get_site_from_url() {
    arr = window.location.href.split('#')
    site = ''
    if (arr.length === 2) {
        site = arr.pop()
    }
    return site
}

var default_site = get_site_from_url()


Vue.component("listpage", {
    template: `
    <table v-show="isShow">
    listpage
    {{ query_site }} 站点信息
    {{ query_site }}
    {{ get_cookies }}  <!-- 更改数据 -->
    {{ total }}
    <tr>
        <td v-for="col in col_list">{{ col }}</td>
    </tr>

    <tr v-for="(item, index) in list_data">
        <td> {{ item.cookies_name }} </td>
        <input :value="item.cookies"  v-model="input_cookies"></input>
        <td> {{ item.modified }} </td>
        <td v-text="item.status?'不可用':'可用'"></td>
        <td :key="item.no">修改</td>
        <td :key="item.no" @click="deleteCookies(item.id, index)">删除</td>
    </tr>

</table>`,
    data() {
        return {
            "list_data": "",
            "input_cookies": "",
            "current_editing_cookies": "",
            "col_list": ["Name", "Cookie", "ModifiedAt", "Status"],
            "total": "",
        }
    },
    props: ["query_site"],
    computed: {
        get_cookies() {
            if (this.query_site != '') {
                axios.get('/cookies_all?site=' + this.query_site).then(response => (
                    this.list_data = response.data.cookies,
                    this.total = response.data.total
                )).catch(function (err) {
                    console.log(err)
                })
            }
        },
        isShow() {
            return this.query_site != ''
        }
    },
    methods: {
        deleteCookies(cookies_id, index) {
            axios.delete('/cookies?cookies_id=' + cookies_id).then(
                response => (this.list_data.splice(index, 1))
            ).catch(response => (''))
        },
        clickToEdite(cookies){
            this.current_editing_cookies =  cookies
            console.log(cookies)
        }
    }

})


var sites = new Vue({
    el: "#site_block",
    data() {
        return {
            "sites": "",
            "total": "",
            "current_query_site": default_site
        }
    },
    mounted() {
        axios.get('/cookies_all_sites').then(response => (
            this.sites = response.data.sites,
            this.total = response.data.total
        )).catch(function (err) {
            console.log(err)
        })
    },
    methods: {
        clickSite(site) {
            this.current_query_site = site
        }
    }
})


