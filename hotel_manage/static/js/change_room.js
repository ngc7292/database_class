var change_room = new Vue({
  el: '#change_room',
  data: {
      method:"change_price",
      room_number:'',
      room_type:'',
      room_price:''
  },
  methods:{
        submit:function(){
          var url="http://127.0.0.1:8000/change_room/";
          var send_data = {
              method:this.$data.method,
              param: {
                  room_number: this.$data.room_number,
                  room_type: this.$data.room_type,
                  room_price: this.$data.room_price
              }};

          axios.post(url,send_data)
            .then(
              response => {
                if(response.data.status == "success") {
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

          }
       }
})