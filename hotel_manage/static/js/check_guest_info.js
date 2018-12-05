var check_info = new Vue({
  el: '#check_info',
  data: {
    members:[{
      name:'',
      id_number:'',
      room_number:''
    }],
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
        add_member:function(){
            this.members.push({
              name:'',
              id_number:'',
              room_number:''
            })
        },
        pop_member:function(){
            if(this.members.length==1)
            {
              alert("查询中必须有一位顾客！！！");
            }
            else
            {
              this.members.pop();
            }
        },
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
  },
})