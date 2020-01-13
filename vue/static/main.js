
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
<div id="show_page">
    <table v-show="isShow">
        {{ get_site_info }}   <!-- 更改数据 -->
        站点信息
        <tr v-for="(site_value,site_key, index) in site_infos">
            <td>{{ site_key }}</td>
            <td>
                <input :value="site_value" v-show="site_key!='modified'"></input>
                <p v-show="site_key==='modified'">{{ site_value }}</p>
            </td>
            <td>    
                <button v-if="site_key==='modified'">修改</button>
                <button v-if="site_key==='modified'">添加</button>
            </td>
        </tr>
    </table>

    <table v-show="isShow">
        {{ get_cookies }}  <!-- 更改数据 -->
        <tr>
            <td v-for="col in col_list">{{ col }}</td>
        </tr>

        <tr>
            <td><input v-model="to_add_cookies_name" placeholder="可留空"></input></td>
            <td><input v-model="to_add_cookies"></input></td>
            <td>-</td>
            <td>-</td>
            <button @click="addCookies(query_site)">添加</button>

        </tr>

        <tr v-for="(item, index) in list_data">
            <td><input :value="item.cookies_name"  @input="inputItem('cookies_name', $event.target.value, index)"></input></td>
            <td><input :value="item.cookies"  @input="inputItem('cookies', $event.target.value, index)"></input></td>
            <td> {{ item.modified }} </td>
            <td v-text="item.status?'不可用':'可用'"></td>
            <button @click="updateItem(index)">修改</button>
            <button @click="deleteCookies(item.id, index)">删除</button>
        </tr>

        <button>上一页</button>
        <input></input>
        <button>下一页</button><p>共{{ total }}条</p>

    </table>
</div>
`
    ,
    data() {
        return {
            "list_data": "",
            "input_cookies": "",
            "current_editing_cookies": "",
            "col_list": ["Name", "Cookie", "ModifiedAt", "Status"],
            "total": "",
            "to_add_cookies_name": "",
            "to_add_cookies": "",
            "site_infos": "",
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
        get_site_info() {
            if (this.query_site != '') {
                axios.get('/cookies_this_site?site=' + this.query_site).then(response => (
                    site = response.data.site,
                    delete site.id,
                    delete site.created,
                    delete site.status,
                    this.site_infos = site
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
                response => (
                    this.list_data.splice(index, 1),
                    alert('删除成功！')
                )
            ).catch(response => (''))
        },
        inputItem(name, input_item, index) {
            this.$set(this.list_data[index], name, input_item)
            this.list_data[index].has_editied = true
            // console.log(input_item, index, this.list_data[index].has_editied)
        },
        updateItem(index) {
            if (this.list_data[index].has_editied === true) {
                var formData = new FormData();
                formData.append('cookies_id', this.list_data[index].id);
                formData.append('cookies', this.list_data[index].cookies);
                formData.append('cookies_name', this.list_data[index].cookies_name);
                axios.put('/cookies', formData).then(
                    response => (
                        alert('修改成功！')
                    )
                ).catch(response => (''))
            } else {
                alert('没有改动，不需要更改！')
            }
        },
        addCookies(query_site) {
            if (!this.to_add_cookies) {
                alert('cookies为空，请填写再添加！')
            } else {
                var formData = new FormData();
                formData.append('site', query_site);
                formData.append('cookies', this.to_add_cookies);
                formData.append('cookies_name', this.to_add_cookies_name);
                axios.post('/cookies', formData).then(
                    response => (
                        alert('添加成功！')
                    )
                ).catch(response => (''))
            }
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


