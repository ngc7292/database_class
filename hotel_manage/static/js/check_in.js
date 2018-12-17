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
              axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
              var url="http://127.0.0.1:8000/check/";
                console.log(this.$data.name);
              axios.post(url,{
                  name:this.$data.name,
                  id_number: this.$data.id_number,
                  room_number: this.$data.room_number,
                  date: this.$data.date
              }).then(function(response){
                  console.log(response);
                  if(response.data.status == "success"){
                      document.getElementById("check_in").reset();
                      alert("succcess");
                  }else {
                      console.log(response.data.msg);
                      alert(response.data.msg);
                  }
                  },function(error){
                  alert("error");
              });
            }
       }
  }
})