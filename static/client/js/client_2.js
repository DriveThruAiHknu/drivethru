function getParameterByName(name) 
{ 
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]"); 
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), 
    results = regex.exec(location.search); 
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " ")); 
}

var carNum = getParameterByName('car');

function my(carNum)
{
    console.log(carNum);
}

my(carNum);