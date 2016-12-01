//Chrome Appointment PUSH Notification start from here
var tId = setInterval(function(){if(document.readyState == "complete") onComplete()},11);
var appointmentData;
function onComplete(){
    clearInterval(tId);    
    getUserAppointment();
    setInterval(function() {
      notify(appointmentData);
    }, 900000 ); 
};
  

Date.prototype.addMinutes= function(h){
    this.setMinutes(this.getMinutes()+h);
    return this;
}

function getUserAppointment(){
        $.ajax({
          dataType: 'JSON',
          type: 'GET',
          url: '/crm/user-appointments/',
          success: function(res) {
              appointmentData = res;
           /*   notify(appointmentData);*/
          },
          error: function(errorThrown) {
          }
      });
    }

function format_time(date_obj) {
  // formats a javascript Date object into a 12h AM/PM time string
  var hour = date_obj.getHours();
  var minute = date_obj.getMinutes();
  var med = (hour > 11) ? "PM" : "AM";
  if(hour > 12) {
    hour -= 12;
  } else if(hour == 0) {
    hour = "12";
  }
  if(minute < 10) {
    minute = "0" + minute;
  }
  return hour + ":" + minute + " "+ med;
}

function notify(data){
  if(data){
    for(var i=0;i<data.length;i++){
    if(data[i]['appointment_time'] != ""){
      var at = new Date(Date.parse(data[i]['appointment_time'])); //Appointment Time
      var ct = new Date(); // Current Time
      if(at > ct && ct.addMinutes(15) > at)
      {
        row = "CID : "+data[i]['customer_id']+"\n"+"Appointment Time : "+ format_time(at);
        notifyMe(row);
      }
    }
  }
  }
}

// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
  if (Notification.permission !== "granted")
    Notification.requestPermission();
});

function notifyMe(row) {
  if (!Notification) {
    alert('Desktop notifications not available in your browser. Please try Google Chrome.'); 
    return;
  }

  if (Notification.permission !== "granted")
    Notification.requestPermission();
  else {
    var notification = new Notification('Hey You have appointment in Next 15 Minutes', {
      body: row,
      icon: notifIcon,
    });
    
  }

}
//Chrome Appointment Notification Ends