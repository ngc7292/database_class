var check_room = new Vue({
  el: '#check_room',
  data: {
    room_types:['双人间'],
    filter:{
      room_type:'',
      room_price:'',
      live_or_book:'',
    },
    rooms:[{
      room_number:'xxx',
      room_type:'xxxx',
      is_live:false,
      is_book:false,
      room_price:100,
      is_show:true,
    }]
  },
  methods:{
        filter_room:function(){
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
        }
  },
})