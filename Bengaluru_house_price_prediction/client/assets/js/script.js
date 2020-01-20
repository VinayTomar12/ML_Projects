// get location:
function onPageLoad(){
  var url = "https://morning-earth-09447.herokuapp.com/locations";
  $.get(url, function(data, status){
    console.log("got response for get_location_names request");
    if(data) {
      var locations = data.locations;
      var uilocations = document.getElementById('sel1');
      $('#sel1').empty();
      for(var i in locations){
        var opt = new Option(locations[i]);
        $('#sel1').append(opt)
      }
    }
  });
}
window.onload = onPageLoad;
// end

function getBHKvalue() {
  var uiBHK = document.getElementsByName("bhk");
  for(var i in uiBHK){
    if(uiBHK[i].checked) {
      return parseInt(i)+1
    }
  }
  return -1
}

function getBathvalue() {
  x = document.getElementById("myRange")
  return parseInt(x.value)
}

function PredictPrice(){
  console.log("Predict price button clicked")
  var bhk = getBHKvalue();
  var bath = getBathvalue();
  var location = document.getElementById("sel1");
  var sqft = document.getElementById("sqft").value;
  var preprice = document.getElementById("uiPredictPrice");
  console.log("Values: bhk:"+bhk+" bath: "+bath+" sqft:"+sqft);
  var url = "https://morning-earth-09447.herokuapp.com/predict_home_price";
  $.post(url, {
     location:location.value,
     total_sqft: parseFloat(sqft),
     bhk : bhk,
     bath : bath
  }, function(data, status){
    preprice.innerHTML = "<h1>"+data.estimated_price+" Lakh INR</h1>"
    // preprice.innerHTML = "<h2>"+data.estimated_price.to_string()+"Lakh INR</h2>"; 
    console.log(status);
});
  return  false
}





var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value; // Display the default slider value

      // Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
}


