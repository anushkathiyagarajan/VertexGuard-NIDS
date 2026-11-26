function drawTrafficChart(normal, attacks){

const ctx = document.getElementById("trafficChart");

new Chart(ctx,{

type:"doughnut",

data:{
labels:["Normal Traffic","Attack Traffic"],

datasets:[{

data:[normal,attacks],

backgroundColor:[
"#22c55e",
"#ef4444"
]

}]

},

options:{
responsive:true,
maintainAspectRatio:false
}

});

}



function drawFeatureChart(features, importance){

const ctx = document.getElementById("featureChart");

new Chart(ctx,{

type:"bar",

data:{

labels:features,

datasets:[{

label:"Feature Importance",

data:importance,

backgroundColor:"#3b82f6"

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

scales:{
y:{
beginAtZero:true
}
}

}

});

}



function drawConfidenceChart(confidence){

const ctx = document.getElementById("confidenceChart");

new Chart(ctx,{

type:"line",

data:{

labels:confidence.map((_,i)=>"Row "+(i+1)),

datasets:[{

label:"Prediction Confidence %",

data:confidence,

borderColor:"#facc15",

backgroundColor:"#facc15",

fill:false

}]

},

options:{
responsive:true,
maintainAspectRatio:false
}

});

}

function drawConfidenceChart(normal, attack){

const ctx = document.getElementById("confidenceChart");

new Chart(ctx,{

type:"bar",

data:{

labels:["Normal Confidence","Attack Confidence"],

datasets:[{

label:"Prediction Confidence %",

data:[normal,attack],

backgroundColor:[
"#22c55e",
"#ef4444"
]

}]

},

options:{
responsive:true,
maintainAspectRatio:false
}

});

}
function drawConfidenceChart(normalConf, attackConf){

const ctx = document.getElementById("confidenceChart").getContext("2d");

new Chart(ctx,{
type:"bar",
data:{
labels:["Normal Confidence","Attack Confidence"],
datasets:[{
label:"Prediction Confidence %",
data:[normalConf,attackConf],
backgroundColor:["#4CAF50","#FF5252"]
}]
},
options:{
responsive:true,
scales:{
y:{
beginAtZero:true,
max:100
}
}
}
});
}