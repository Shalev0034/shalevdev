window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    $.post( "/updateTable", {
    javascript_data: document.documentElement.innerHTML,
    date: document.getElementById('calender-date').innerHTML
});
});

let typingTimer;                //timer identifier
let doneTypingInterval = 300;  //time in ms (5 seconds)
//on keyup, start the countdown
document.addEventListener('keyup', () => {
    clearTimeout(typingTimer);
   
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
    
});

//user is "finished typing," do something
function doneTyping () {
    $.post( "/updateTable", {
    javascript_data: document.documentElement.innerHTML,
    date: document.getElementById('calender-date').innerHTML

});
}

function bold(){
    document.execCommand("bold"); 
    $.post( "/updateTable", {
    javascript_data: document.documentElement.innerHTML,
    date: document.getElementById('calender-date').innerHTML

});  
}

function underline(){
    document.execCommand("underline");
    $.post( "/updateTable", {
    javascript_data: document.documentElement.innerHTML,
    date: document.getElementById('calender-date').innerHTML

});
}

function italic(){
    document.execCommand("italic")
    $.post( "/updateTable", {
    javascript_data: document.documentElement.innerHTML,
    date: document.getElementById('calender-date').innerHTML

});
}

function changeFontColor(){
document.execCommand("foreColor",false,document.getElementById('colorpicker').value);
    $.post( "/updateTable", {
    javascript_data: document.documentElement.innerHTML,
    date: document.getElementById('calender-date').innerHTML

});
}

function changeBackColor(){
    document.execCommand("backColor",false,document.getElementById('colorpicker').value);
    $.post( "/updateTable", {
    javascript_data: document.documentElement.innerHTML,
    date: document.getElementById('calender-date').innerHTML

});
}

function addMajor(){
    $.post( "/addMajor", {
    javascript_data: document.getElementById('selectMajor').value
});
window.location.reload()

}
 
function deleteMajor(id){
 $.post( "/deleteMajor", {
    javascript_data: id
});
window.location.reload()
}


function submit(){
    document.getElementById('selectKeyWord').submit();
}

function removeKeyWord(keywordButton){
     $.post( "/removeKeyWord", {
    keyword: keywordButton
});
window.location.reload()
}