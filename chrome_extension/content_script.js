handleSummaryDisplay();

function handleSummaryDisplay() {
    var summaryDiv = document.getElementById("TLDR_blanket");
    if(summaryDiv == null) {
	    requestSummary();
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

function sendRequest(url) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://news-article-summarizer.herokuapp.com/summary_api/", true);
    xhr.onreadystatechange = function() {
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var summary = xhr.responseText;
            arr = summary.split('@');
            title = 'Summary';
            if(arr.length > 1) {
                title = arr[0];
                summary = arr[1];
                console.log('title: ' + title);
                console.log('summary: ' + summary);
            }
	        showSummary(summary, title);
	    }
    }
    var pos = url.indexOf(".html");
    if(pos != -1)
    {
        url = url.substring(0,pos + 5);
    }
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send("url=" + url);
}

function getArticleSummary() {
    url = document.URL;
    //sendRequest(url);
    var hardcodedArticle = "This is some hardcoded stuff. ~For someone who\'s only used it twice, President Obama may need some reacquainting with the last remaining weapon in Democrats\' arsenal.~ He last rejected a bill from Congress in 2010.~\
But he\'s had blocking from a Democratic Senate majority until now. ~They\'ve stood in the way of bills most Democrats would oppose.~ Things are likely to change in JanuarRepublicans take charge of the Senate.~\
If Senate Republicans follow the path of their House counterparts, he could be faced with proposals to repeal Obamacare and budgets that cut entitlement programs - the type of bills that will meet a quick end at the other end of Pennsylvania Avenue.~who\'s only used it twice, President Obama may need some reacquainting with the last remaining weapon in Democrats\' arsenal.~ He last rejected a bill from Congress in 2010.~\
But he\'s had blocking from a Democratic Senate majority until now.~ They\'ve stood in the way of bills most Democrats would oppose.~ Things are likely to change in January, when Republicans take charge of the Senate. ~\
If Senate Republicans follow the path of their House counterparts, he could be faced with proposals to repeal Obamacare and budgets that cut entitlement programs - the type of bills that will meet a quick end at the other end of Pennsylvania Avenue.";
    var titleArr = document.getElementsByClassName('headline');
    var title = "";
    if(titleArr.length != 0) {
	    title = titleArr[0].innerText;
    }
    else {
	    title = "Summary title goes here";
    }
    
    showSummary(hardcodedArticle, title);
}

function showLoadingAnimation() {
    var img = document.createElement('img');
    img.id = "TLDR_loading_image";
    img.style.cssText = "position: fixed; z-index: 2000000000; top: 47%; left: 47%;";
    img.src = chrome.extension.getURL("circle-loading-animation.gif");
    document.body.appendChild(img);
}

function hideLoadingAnimation() {
    var img = document.getElementById("TLDR_loading_image");
    img.style.display = "none";
}

function requestSummary() {
    showLoadingAnimation();
    sendRequest(document.URL);
}

function makeUl(summaryText) {
    var ret = '<ul style="list-style-type: lower-greek;">';
    sentenceArr = summaryText.split('~');
    for(i = 0; i < sentenceArr.length; i++) {
	    ret += '<li>';
	    ret += sentenceArr[i];
	    ret += '</li>';
    }
    ret += "</ul>";
    return ret;
}

function showSummary(summary, title) {
    hideLoadingAnimation();
    var newDiv = document.createElement('div');
    newDiv.id = "TLDR_blanket";
    newDiv.className="tb-container";
    summary = makeUl(summary);
    var html = '\
<div class="TLDR_content tb-container" style="\
width: 50%;\
height: 90%;\
position: relative;\
background: white;\
left: 25%;\
padding: 3%;\
padding-bottom: 2%;\
padding-top: 2%;\
font-size: 16px; \
box-sizing: border-box;\
top: 5%;\
overflow-y:scroll; \
text-align: justify;\
">\
<h1 class="tb-container" style="text-align: center; padding-bottom: 8px;" >' + title + '</h1>\
<div class="TLDR_summary tb-container">' + summary + '\
\
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

    //    add bootstrap
    var ss = document.createElement("link");
    ss.rel = "stylesheet";
    // ss.href = "http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css";
    ss.href = "chrome-extension://efdchehaeenfdpneibdngkkpdpjmping/bootstrap/css/bootstrap.min.prefixed.css"
    document.getElementsByTagName("head")[0].appendChild(ss);
    
}
