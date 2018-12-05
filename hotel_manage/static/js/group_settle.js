var check_in = new Vue({
  el: '#settle',
  data: {
    org_name:'',
    show_table:false,
    orders:[{
      id:'1',
      id_number:'xxxxxxxxxxxxxxxxxx',
      name:'xxx',
      room_number:'xxx',
      date:'xxxx-xx-xx',
      price:122
    }]
  },
  methods:{
        submit_guest:function(){
            var send_data=JSON.stringify(this.$data);
            var url="http://localhost/group_book";
            axios.get('https://ngc7292.github.io/')
            .then(
              response => {
                document.getElementById("settle-form").reset();
                alert("success");
                this.show_table=true;
            },function(error){
                alert("error");
            });
        },
        submit_order:function(){
            var send_data=JSON.stringify(this.$data);
            var url="http://localhost/group_book";
            axios.get('https://ngc7292.github.io/')
            .then(
              response => {
                alert("success");
            },function(error){
                alert("error");
            });
        },
  },
})