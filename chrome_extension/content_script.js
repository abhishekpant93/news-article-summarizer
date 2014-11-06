
handleSummaryDisplay("null", "null");

function handleSummaryDisplay() {
    var summaryDiv = document.getElementById("TLDR_blanket");
    if(summaryDiv == null) {
	showSummary("null", "null");
    }
    else {
	flipSummaryDisplay(summaryDiv);
    }
}

function flipSummaryDisplay(div) {
    if(div.style["display"] == "none") {
	div.style["display"] = "initial";
	}
    else(div.style.display = "none");
    }

function showSummary(title, text) {
    var newDiv = document.createElement('div');
    newDiv.id = "TLDR_blanket";
    var html = '\
<div class="TLDR_content" style="\
width: 50%;\
height: 90%;\
position: relative;\
background: rgb(221, 239, 255);\
left: 25%;\
padding: 5%;\
padding-bottom: 2%;\
padding-top: 2%;\
box-sizing: border-box;\
top: 5%;\
font-family: Times New Roman; \
line-height: 120%; \
overflow-y:scroll; \
text-align: justify;\
">\
<h1 style="text-align: center; font-family: Arial; padding-bottom: 8px;" >Summary title goes here</h1>\
<div class"TLDR_summary">\
This is some hardcoded stuff. For someone who\'s only used it twice, President Obama may need some reacquainting with the last remaining weapon in Democrats\' arsenal. He last rejected a bill from Congress in 2010.\
But he\'s had blocking from a Democratic Senate majority until now. They\'ve stood in the way of bills most Democrats would oppose. Things are likely to change in JanuarRepublicans take charge of the Senate.\
If Senate Republicans follow the path of their House counterparts, he could be faced with proposals to repeal Obamacare and budgets that cut entitlement programs - the type of bills that will meet a quick end at the other end of Pennsylvania Avenue.who\'s only used it twice, President Obama may need some reacquainting with the last remaining weapon in Democrats\' arsenal. He last rejected a bill from Congress in 2010.\
But he\'s had blocking from a Democratic Senate majority until now. They\'ve stood in the way of bills most Democrats would oppose. Things are likely to change in January, when Republicans take charge of the Senate.\
If Senate Republicans follow the path of their House counterparts, he could be faced with proposals to repeal Obamacare and budgets that cut entitlement programs - the type of bills that will meet a quick end at the other end of Pennsylvania Avenue.\
</div>\
</div>\
\
'


    newDiv.onclick = function(event){
	var wid = event.clientX, scrWid = document.body.clientWidth;
	if (wid < scrWid*0.25 || wid > scrWid*0.75)
	    this.style['display'] = "none";	
    }
    newDiv.innerHTML = html;
    var styleString = "\
background: rgba(0, 0, 0, 0.7);\
width: 100%;\
height: 100%;\
position: fixed;\
z-index:2147483647;\
top: 0;\
left: 0;\
";
    newDiv.style.cssText = styleString;
    document.body.appendChild(newDiv);
}
