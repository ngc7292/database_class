var check_in = new Vue({
  el: '#check_in',
  data: {
    name:'',
    id_number:'',
    room_number:'',
    date:get_date(),
  },
  methods:{
        submit:function(){

            if(!check_date(this.date))
            {
              alert("您输入的日期有误，请输入今日或之后的日期，若日期位于今日之后，即为预定房间。");
            }
            else
            {
              var send_data=JSON.stringify(this.$data);
              var url="http://localhost/group_book";
              console.log(this);
  
              axios.get('https://ngc7292.github.io/').then(function(response){
                  document.getElementById("check_in").reset();
                  alert("success");
              },function(error){
                  alert("error");
              });
            }
       }
  }
})