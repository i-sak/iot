let video;
let classifier;
let label;

function preload(){
  //Tensorflow.js->Upload->Your sharable link
  //링크 + model.json
  classifier = ml5.imageClassifier('https://teachablemachine.withgoogle.com/models/IVLNh0lTi/model.json');
}

function setup() {
  createCanvas(340, 270);
  video = createCapture(VIDEO);
  video.hide();
  
  classfiyVideo();
}

function classfiyVideo(){
  classifier.classify(video, gotResult);
}
function draw() {
  background(0);
  image(video, 0,0);
  
  textSize(32);
  textAlign(CENTER, CENTER);
  fill(0);
  text(label, width/2, height/2);
}

function gotResult(error, results){
  if(error){
    console.log(error);
    return;
  }
  //모든 클래스 다 나오고 싶을 때
  //console.log(results);
  
  console.log(results[0].label);
  label = results[0].label;
  
  classfiyVideo();
}