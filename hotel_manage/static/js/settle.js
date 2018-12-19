var check_in = new Vue({
  el: '#settle',
  data: {
    name:'',
    id_number:'',
    show_table:false,
    orders:[]
  },
  methods:{
        submit_guest:function(){
            var send_data=JSON.stringify(this.$data);
            var url="http://127.0.0.1:8000/settle/";
            axios.post(url,{
                name:this.$data.name,
                id_number:this.$data.id_number
            })
            .then(
              response => {
                if(response.data.status == "success") {
                    console.log(response.data.orders);
                    this.show_table = true;
                    for(order in response.data.orders){
                        this.orders.push(response.data.orders[order]);
                    }
                    alert("success");
                }
                else if(!response.data.msg){
                    console.log(response);
                    alert("no this guest")
                }
                else{
                    alert("error")
                }
            },function(error){
                alert("error");
            });
        },
        submit_order:function(){
            var send_data=[];
            for(order in this.$data.orders)
            {
                send_data.push(this.$data.orders[order].id);
            }
            console.log(send_data);
            var url="http://127.0.0.1:8000/settle_finish/";
            axios.post(url, {order_id:send_data})
            .then(
              response => {
                if(response.data.status == "success"){
                    alert("success");
                    window.location.href("http://127.0.0.1:8000/")
                }
                else{
                    alert("error");
                }
            },function(error){
                alert("error");
            });
        },
  },
})