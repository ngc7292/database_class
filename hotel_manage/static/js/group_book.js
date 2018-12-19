var group_book_method = new Vue({
  el: '#group_book',
  data: {
    org_name: '',
    members:[{
        name:'',
        id_number:'',
        room_number:''
    }],
    date:get_date(),
  },
  methods:{
        addmember:function(){
            this.members.push({
              name:'',
              id_number:'',
              room_number:''
            })
        },
        popmember:function(){
            if(this.members.length==1)
            {
              alert("团体登记以及预定时必须有一位顾客！！！");
            }
            else
            {
              this.members.pop();
            }
        },
        submit:function(){
            if(!check_date(this.date))
            {
              alert("您输入的日期有误，请输入今日或之后的日期，若日期位于今日之后，即为预定房间。");
            }
            else
            {
              var url="http://127.0.0.1:8000/group/";
  
              axios.post(url, this.$data).then(response => {
                  if(response.data.status == "success")
                  {
                      alert("success");
                  }
                  else
                  {
                      alert("error")
                  }
              },function(error){
                  alert("error");
              });
            }
       }
  }
})