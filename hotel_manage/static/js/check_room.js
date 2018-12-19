var check_room = new Vue({
  el: '#check_room',
  data: {
    rooms:[]
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