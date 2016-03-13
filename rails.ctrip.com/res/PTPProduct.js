var pageid = '103112';
var validateShow;
var dropAdult = 1, dropChild = 0, dropYouth = 0, dropSeniors = 0;
var LastTimeLow = "", LastBackTimeLow = "";
var noResult = 0;
var isRunning = false;
var requestParameter;
var host;
var address;
var applicationAddress;
var currentButton;
var lastScrollTop = 0;
var IsStartCityTW = false;
var isBrowerBack = false;
//台湾高铁售卖日期调整为周五 T+4 ~ T+27，其余T+3 ~ T+27
//台铁下单日期开始
var trainAddDaysFrom = 3;
//台铁下单日期结束
var trainAddDaysTo = 27;
//欧铁出发日期
var OTStartDate = 1;
var OTBackDate = 8;
var OTDefaultStartDate = 7;
var OTDefaultBackDate = 15;
//点对点人数变量
var totalNumbers = 9;
var adultsPassengerNumbers = 2;
var childrenPassengerNumbers = 0;
var youthPassengerNumbers = 0;
var elderPassengerNumbers = 0;
//默认不在区域中
var isOut = true;
var zuoweiisOut = true;
var traveTypeisOut = true;
var depTimeisOut = true;
var backTimeisOut = true;
//出发时间显示层控制
var depTimeIsShow = 0;
//返回时间显示层控制
var backTimeIsShow = 0;
//是否加载页面
var IsLoadPage = 0;
$.ready(function () {
    applicationAddress = $("#applicationAddress").value();
    PTPMyProcess.ShowValidateCode();
    if (parseInt(IsLoadPage, 10) > 0) {
        return false;
    }
    LoadInit();
});
var LoadInit = function () {
    applicationAddress = $("#applicationAddress").value();
    var nowDay = new Date().getDay();
    if (nowDay && parseInt(nowDay) == 5) {
        trainAddDaysFrom = 4;
    }
    PTPMyProcess.Init();
    CheckStartCity();
    host = $("#hostAddress").value();
    requestParameter = $.parseJSON($("#requestParameter").value());
    $.mod.load('jmp', '1.0');
    $.mod.load('notice', '1.1');
    $(document).regMod('jmp', '1.0', {});
    $.mod.load('validate', '1.1', function () {
        var valid = $(document).regMod("validate", '1.1');
        validateShow = function (obj, message) {
            setTimeout(function () {
                valid.method("show", { $obj: obj, data: message, removeErrorClass: true, hideEvent: "blur", isFocus: true });
            })
            return false;
        };
    });
    var passHolders = global.getQueryStringByName('passHolders') || requestParameter.PassHolders;
    if (passHolders !== "0") {
        address = "seatres/";
        $("#dropPassHolders").css("display", "");
        $("#txtPtpNumber").css("display", "none");
        global.regAddressZuoWei("#txtCityDep", "txtCityDep", "#hdstCode", "#hdstName", applicationAddress);
        global.regAddressZuoWei("#txtCityAri", "txtCityAri", "#hddtCode", "#hddtName", applicationAddress);
    }
    else {
        address = "ptp/";
        $("#dropPassHolders").css("display", "none");
        $("#txtPtpNumber").css("display", "");
        // $(".search_item").css("display", "");
        //$(".pe_explain").css("display", "");
        //$($(".zuowei_search_item")[0]).css("display", "none");
        global.regAddressNew("#txtCityDep", "txtCityDep", "#hdstCode", "#hdstName", applicationAddress);
        global.regAddressNew("#txtCityAri", "txtCityAri", "#hddtCode", "#hddtName", applicationAddress);
    }

    $("#txtDateDep").value((new Date()).addDays(OTDefaultStartDate).toFormatString('yyyy-MM-dd'));
    $("#txtDateAri").value((new Date()).addDays(OTDefaultBackDate).toFormatString('yyyy-MM-dd'));
    global.regDate("#txtDateDep", ((new Date()).addDays(OTStartDate).toFormatString('yyyy-MM-dd')), (new Date()).addDays(180).toFormatString('yyyy-MM-dd'));
    global.regDate("#txtDateAri", ((new Date()).addDays(OTStartDate).toFormatString('yyyy-MM-dd')), (new Date()).addDays(180).toFormatString('yyyy-MM-dd'));
    $("#trainTxtDateDep").value((new Date()).addDays(trainAddDaysFrom).toFormatString('yyyy-MM-dd'));
    global.regDate("#trainTxtDateDep", ((new Date()).addDays(trainAddDaysFrom).toFormatString('yyyy-MM-dd')), (new Date()).addDays(trainAddDaysTo).toFormatString('yyyy-MM-dd'));
    if (requestParameter.DepartureDate || global.getQueryStringByName("departureDate")) {
        $("#txtDateDep").value(requestParameter.DepartureDate || global.getQueryStringByName("departureDate"));
        $("#trainTxtDateDep").value(requestParameter.DepartureDate || global.getQueryStringByName("departureDate"));
    }
    if (global.getQueryStringByName("arriveDate") || requestParameter.ArrivalDate) {
        $("#txtDateAri").value(requestParameter.ArrivalDate || global.getQueryStringByName("arriveDate"));
    }
    $("#pop-box .c_close").bind("click", function () {
        $('#pop-box').unmask();
    });
    $("#pop-box .btn_s").bind("click", function () {
        var pageStatus = $("#pageStatus").value();
        var id = currentButton.attr("PkgID");
        if (pageStatus == "1") {
            var data = currentButton.attr("callback-data");
            var params = getParams();
            var transferParams = getTransferParams(params);
            $.extend(transferParams, { pageStatus: "2" });
            var array = [];
            var arraySet = [];
            for (var attr in transferParams) {
                array.push(attr + "$" + transferParams[attr]);
                if (attr != "from" && attr != "to" && attr != "startCityName" && attr != "destCityName") {
                    arraySet.push(attr + "=" + transferParams[attr]);
                }
            }
            var queryString;
            if (transferParams["from"] && transferParams["to"]) {
                queryString = transferParams["from"] + "-" + transferParams["to"];
                queryString += "?";
            }
            queryString += arraySet.join("&");
            var url = host + address + queryString; //测试改成applicationAddress,测试后改成host
            var hidStr = currentButton.nextSibling();
            if (hidStr) {
                $("#hidData").value($(hidStr).value());
                array.push("firstTrain" + "$" + $("#hidData").value());
            }
            var bookData = cQuery.parseJSON($("#hidBookData").value())
            for (var i = 0; i < bookData.length; i++) {
                if (bookData[i].PackagePrices.PackageFareId == id) {
                    array.push("bookData" + "$" + cQuery.stringifyJSON(bookData[i]));
                    break;
                }
            }
            StandardPost(url, array);
        }
        {
            $('#pop-box').unmask();
            __SSO_booking(currentButton, 0);
        }
    });
    $("#pop-box .btn_c").bind("click", function () {
        $('#pop-box').unmask();
    });

    $("#txtCityDep").bind("blur", function (e) {
        CheckStartCity();
    });


    GetPTPQuestionList();
    initSearchBar();
    isBrowerBack = !!$.pageStorage.get('LastTimeLow');
    if (isBrowerBack) {
        Search();
    }
    else {
        GetPTPProductList();
    }
    SortBindAndTrigger();
    window.onscroll = function () {
        if (lastScrollTop > getScrollTop()) {
            lastScrollTop = getScrollTop();
            return false;
        }
        lastScrollTop = getScrollTop();
        if ((getScrollTop() + getClientHeight() + 400) >= getScrollHeight()) {
            //alert("到达底部");
            if (noResult == 0 && !isRunning) {
                GetPTPProductList();
            }
        }
    };
    PTPMyProcess.ProShowPassengerNumber();
    //$("#goDetails").regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '280', minWidth: '280' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_Rule', content: getTitleTips($("#goDetails").attr("refund"))} });

}

var historyBack = function () {
    var params = getParams();
    delete params.data;
    params.child = params.children;
    params.adult = params.adults;
    delete params.children;
    delete params.adults;
    $.extend(params, { pageStatus: "1", from: params.fromCityCode, to: params.toCityCode });
    delete params.fromCityCode;
    delete params.toCityCode;
    var queryString;
    if (params["from"] && params["to"]) {
        queryString = params["from"] + "-" + params["to"];
        queryString += "?";
    }
    if (params["departureDate"]) {
        queryString += "departureDate" + "=" + params["departureDate"];
        queryString += "&";
    }
    if (params["departureTimeLow"] && params["departureTimeHigh"]) {
        queryString += "starttime" + "=" + params["departureTimeLow"] + "-" + params["departureTimeHigh"];
        queryString += "&";
    }
    if (params["searchType"]) {
        queryString += "searchType" + "=" + params["searchType"];
        queryString += "&";
    }
    if (params["searchType"] == 1) {
        if (params["arriveDate"]) {
            queryString += "arriveDate" + "=" + params["arriveDate"];
            queryString += "&";
        }
        if (params["backTimeLow"] && params["backTimeHigh"]) {
            queryString += "backtime" + "=" + params["backTimeLow"] + "-" + params["backTimeHigh"];
            queryString += "&";
        }
    }
    if (params["passHolders"] == 0) {
        if (params["adult"]) {
            queryString += "adult" + "=" + params["adult"];
            queryString += "&";
        }
        if (params["child"]) {
            queryString += "child" + "=" + params["child"];
            queryString += "&";
        }
        if (params["youth"]) {
            queryString += "youth" + "=" + params["youth"];
            queryString += "&";
        }
        if (params["seniors"]) {
            queryString += "seniors" + "=" + params["seniors"];
            queryString += "&";
        }
        queryString += "passHolders" + "=" + params["passHolders"];
    }
    else {
        queryString += "passHolders" + "=" + params["passHolders"];
        queryString += "&";
    }
    //        if (params["pageStatus"] == 2) {
    //            queryString += "pagestatus2";
    //            queryString += "/";
    //        }
    var url = host + address + queryString;
    window.location.href = url;
}

var BookingCheck = function (btn) {
    try {
        //埋点--点击预订按钮时触发
        if (typeof window['__bfi'] == 'undefined') window['__bfi'] = [];
        window['__bfi'].push(['_tracklog', 'train_outie_list_book_online', "{'uid':'${duid}','page_id':'${page_id}','VERSION':'1','starcity':'" + $("#hdstCode").value() + "','arrivecity':'" + $("#hddtCode").value() + "','starttime':'" + $("#txtDateDep").value() + "','traveltype':'" + $("#MaiDianTravelType").value() + "'}"]);
    }
    catch (ex)
    { }


    var local = btn;
    var pageStatus = $("#pageStatus").value();
    var id = $(local).attr("PkgID");
    if (pageStatus == "1") {
        var passHolders = global.getQueryStringByName('passHolders');
        if ($(local).attr("PassChecked") != "False" && passHolders == "0") {
            currentButton = $(local);
            $('#pop-box').mask();
            return;
        }
        var data = $(local).attr("callback-data");
        var params = getParams();
        var transferParams = getTransferParams(params);
        $.extend(transferParams, { pageStatus: "2" });
        var array = [];
        var arraySet = [];
        for (var attr in transferParams) {
            array.push(attr + "$" + transferParams[attr]);
            if (attr != "from" && attr != "to" && attr != "startCityName" && attr != "destCityName") {
                arraySet.push(attr + "=" + transferParams[attr]);
            }
        }
        var queryString;
        if (transferParams["from"] && transferParams["to"]) {
            queryString = transferParams["from"] + "-" + transferParams["to"];
            queryString += "?";
        }
        queryString += arraySet.join("&");
        var url = host + address + queryString; //测试改成applicationAddress,测试后改成host
        var hidStr = $(local).nextSibling();
        if (hidStr) {
            $("#hidData").value($(hidStr).value());
            array.push("firstTrain" + "$" + $("#hidData").value());
        }
        var bookData = cQuery.parseJSON($("#hidBookData").value())
        for (var i = 0; i < bookData.length; i++) {
            if (bookData[i].PackagePrices.PackageFareId == id) {
                array.push("bookData" + "$" + cQuery.stringifyJSON(bookData[i]));
                break;
            }
        }
        StandardPost(url, array);
        //记录最后刷新时间
        $.pageStorage.clear();
        $.pageStorage.set('LastTimeLow', document.getElementById("sltDepTime").value);
        global.preventDefault();
    }
    else {
        var passHolders = global.getQueryStringByName('passHolders');
        if ($(local).attr("PassChecked") != "False" && passHolders == "0") {
            currentButton = $(local);
            $('#pop-box').mask();
            return;
        }

        //记录最后刷新时间
        $.pageStorage.clear();
        $.pageStorage.set('LastTimeLow', document.getElementById("sltDepTime").value);
        global.preventDefault();
        return __SSO_booking($(local), 0);
    }

}

function getTransferParams(params) {
    var value = {};
    value.adult = params.adults;
    value.child = params.children;
    value.seniors = params.seniors;
    value.youth = params.youth;

    value.departureDate = params.departureDate;
    value.starttime = params.departureTimeLow + "-" + params.departureTimeHigh;
    value.from = params.fromCityCode;
    value.startCityName = $("#txtCityDep").value();
    value.destCityName = $("#txtCityAri").value();
    value.passHolders = params.passHolders;
    value.to = params.toCityCode;
    value.searchType = params.searchType;
    value.arriveDate = params.arriveDate;
    value.backtime = params.backTimeLow + "-" + params.backTimeHigh;
    value.pageStatus = params.pageStatus;
    return value;
}

function initSearchBar() {

    var value = getParams();
    adultsPassengerNumbers = value.adults;
    childrenPassengerNumbers = value.children;
    youthPassengerNumbers = value.youth;
    elderPassengerNumbers = value.seniors;
    $("#passengerNumber1").value(value.children);
    $("#passengerNumber2").value(value.youth);
    $("#passengerNumber3").value(value.adults);
    $("#passengerNumber4").value(value.seniors);

    dropAdult = value.adults;
    dropChild = value.children;
    dropYouth = value.youth;
    dropSeniors = value.seniors;

    if (value.searchType == 0 || value.searchType == 1) {
        $("#selTravelType").value(value.searchType);
        PTPMyProcess.Hide("ulTraveType");
        if (value.searchType == 0) {
            $("#traveTypeText").html("单程");
            if (!$($("#txtDateAri").parentNode()).hasClass("disabled")) {
                $($("#txtDateAri").parentNode()).addClass("disabled");
            }
        }
        else if (value.searchType == 1) {
            $("#traveTypeText").html("往返");
            if ($($("#txtDateAri").parentNode()).hasClass("disabled")) {
                $($("#txtDateAri").parentNode()).removeClass("disabled");
            }
        }
    }

    $('#sltDepTime').value(value.departureTimeLow + "-24:00");
    $('#sltAriTime').value(value.backTimeLow + "-24:00");
    $('#dTimeTxt').value(value.departureTimeLow);
    $('#bTimeTxt').value(value.backTimeLow);
}

function getParams(params) {
    var fromCity = requestParameter.DepartureCity || global.getQueryStringByName('from') || (params !== undefined ? params["from"] : "");
    var toCity = requestParameter.ArrivalCity || global.getQueryStringByName('to') || (params !== undefined ? params["to"] : "");
    var departureDate = requestParameter.DepartureDate || global.getQueryStringByName("departureDate") || (params !== undefined ? params["departureDate"] : new Date().toDateString());
    var arriveDate = requestParameter.ArrivalDate || global.getQueryStringByName('arriveDate') || (params !== undefined ? params["arriveDate"] : "");
    var starttime = requestParameter.StartTime || global.getQueryStringByName('starttime') || (params !== undefined ? params["starttime"] : '06:00-12:00');
    var departureTimeHigh = starttime.split("-")[1];
    var departureTimeLow = starttime.split("-")[0];
    var searchType = requestParameter.SearchType || global.getQueryStringByName('searchType') || (params !== undefined ? params["searchType"] : 0);
    var backtime = requestParameter.BackTime || global.getQueryStringByName('backtime') || (params !== undefined ? params["backtime"] : '06:00-12:00');
    var backTimeHigh = backtime.split("-")[1];
    var backTimeLow = backtime.split("-")[0];
    var pageStatus = $("#pageStatus").value();
    var data = global.getQueryStringByName('data') || "" || requestParameter.Data;
    var startCityName = $("#hdstName").value();
    var destCityName = $("#hddtName").value();
    var passHolders = requestParameter.PassHolders || global.getQueryStringByName('passHolders') || (params !== undefined ? params["passHolders"] : 0);
    var value = {};
    value.adults = requestParameter.adult || global.getQueryStringByName('adult') || (params !== undefined ? params["adult"] : "1");
    value.children = requestParameter.child || global.getQueryStringByName('child') || (params !== undefined ? params["child"] : "0");
    value.seniors = requestParameter.seniors || global.getQueryStringByName('seniors') || (params !== undefined ? params["seniors"] : "0");
    value.youth = requestParameter.youth || global.getQueryStringByName('youth') || (params !== undefined ? params["youth"] : "0");
    value.departureDate = departureDate;
    value.departureTimeHigh = departureTimeHigh;
    value.departureTimeLow = departureTimeLow;
    value.fromCityCode = fromCity;
    value.toCityCode = toCity;
    value.arriveDate = arriveDate;
    value.startCityName = startCityName;
    value.destCityName = destCityName;
    value.backTimeHigh = backTimeHigh;
    value.backTimeLow = backTimeLow;
    value.passHolders = 0;
    value.searchType = searchType;
    value.pageStatus = pageStatus;
    value.data = data;
    value.passHolders = passHolders;
    if (value.passHolders !== "0") {
        value.adults = "0";
        value.children = "0";
        value.seniors = "0";
        value.youth = "0";
    }
    return value;

}

var GetPTPQuestionList = function () {
    cQuery.ajax(applicationAddress + "Ajax/PTPProductListHandler.ashx?Action=QureyAnswerResponse",
             {
                 method: 'POST',
                 timeout: 3000,
                 context: 'value={\"Type\":\"2\"}',
                 async: false,
                 onsuccess: function (result) {
                     var data = cQuery.parseJSON(result.responseText); //强制转换一下json字符串，生成json对象
                     if (data != null && data.AnswerList != null && data.AnswerList.length > 0) {
                         var questions = "";
                         for (i = 0; i < data.AnswerList.length; i++) {
                             questions += "<li><a target='_blank' href=" + host + "ask/" + data.AnswerList[i].ID + ".html>" + (i + 1) + "." + data.AnswerList[i].Question + "</a></li>";
                         }
                         $("#ulQuestions").html(questions);
                     }
                 },
                 onerror: function () { }
             });
};

var GetPTPProductList = function (params) {

    isRunning = true;
    $("#searchLoading").css("display", "");
    var value = getParams(params);

    if (LastTimeLow != "") {
        value.departureTimeLow = LastTimeLow;
    }

    var pageStatus = $("#pageStatus").value();
    if (pageStatus == "2") {
        var departureDate = value.departureDate;
        var departureTimeHigh = value.departureTimeHigh;
        var departureTimeLow = value.departureTimeLow;
        var fromCity = value.fromCityCode;
        var toCity = value.toCityCode;
        var arriveDate = value.arriveDate;
        var startCityName = value.startCityName;
        var destCityName = value.destCityName;
        var backTimeHigh = value.backTimeHigh;
        var backTimeLow = value.backTimeLow;

        value.departureDate = arriveDate;
        value.departureTimeHigh = backTimeHigh;
        value.departureTimeLow = backTimeLow;
        value.fromCityCode = toCity;
        value.toCityCode = fromCity;
        value.arriveDate = departureDate;
        value.startCityName = destCityName;
        value.destCityName = startCityName;
        value.backTimeHigh = departureTimeHigh;
        value.backTimeLow = departureTimeLow;

        if (LastBackTimeLow != "") {
            value.departureTimeLow = LastBackTimeLow;
        }

        if ($("#hidData").value() != "") {
            value.one = $("#hidData").value();
            $.cookie.set('hidData', 'first', value.one);

        }
        else {
            value.one = $.cookie.get('hidData', 'first');
            //$("#hidData").value(value.one);
        }
        if ($("#hidFirstData").value() != "") {
            value.data = $("#hidFirstData").value();
            $.cookie.set('hidFirstData', 'first', value.data);
        }
        else {
            value.data = $.cookie.get('hidFirstData', 'first');
        }
        if ($("#hidBookData").value() != "") {
            value.BookData = $("#hidBookData").value();
            if ($("#tbodyProductList").html().trim() == "") {
                $.cookie.set('hidBookData', 'first', value.BookData);
                if (!($.cookie.set('hidBookData', 'first'))) {
                    if (localStorage) {
                        localStorage.setItem('hidBookData', value.BookData);
                    }
                }
            }
        }
        else {
            value.BookData = ($.cookie.get('hidBookData', 'first') == "" || $.cookie.get('hidBookData', 'first') == "undefined") ? (localStorage ? localStorage.getItem('hidBookData') : "") : $.cookie.get('hidBookData', 'first');
        }

    }
    else {
        if ($("#hidBookData").value() != "") {
            value.BookData = $("#hidBookData").value();
        }
    }

    if (value != null && value.passHolders == 0)//点对点
    {
        pageid =103112;
    }
    else {//订座
        pageid = 103123;
    }
    //添加pageID
    $("#page_id").value(pageid);

    $("#divNoResult").css("display", "none");
    cQuery.ajax(applicationAddress + "Ajax/PTPProductListHandler.ashx?Action=GetPTPProductList",
             {
                 method: 'POST',
                 timeout: 3000,
                 context: 'value=' + $.stringifyJSON(value),
                 onsuccess: function (result) {
                     isBrowerBack = false;
                     var data = cQuery.parseJSON(result.responseText); //强制转换一下json字符串，生成json对象
                     if (data != null && data != 'undefined') {
                         noResult = data.NoResult;
                         if (data.LastTimeLow) {
                             LastTimeLow = data.LastTimeLow;
                         }
                         if (data.LastBackTimeLow) {
                             LastBackTimeLow = data.LastBackTimeLow;
                         }
                         if (data.ShowHtml != "") {
                             $("#tbodyProductList").html($("#tbodyProductList").html() + data.ShowHtml);
                             //$("#tbodyProductList").append(data.ShowHtml);
                             $("#divNoResult").css("display", "none");

                         }
                         else {
                             if ($("#tbodyProductList").html().trim() == "") {
                                 $("#divNoResult").css("display", "");
                                 $("#searchLoading").css("display", "none");
                                 try {
                                     //埋点
                                     if (typeof window['__bfi'] == 'undefined') window['__bfi'] = [];
                                     window['__bfi'].push(['_tracklog', 'train_outie_list_nonresult_online', "{'uid':'${duid}','page_id':'${page_id}','VERSION':'1','starcity':'" + $("#hdstCode").value() + "','arrivecity':'" + $("#hddtCode").value() + "','starttime':'" + $("#txtDateDep").value() + "','traveltype':'" + $("#MaiDianTravelType").value() + "'}"]);
                                 }
                                 catch (ex) { }


                             }
                         }
                         $("#hidBookData").value(data.BookingData);

                         var passHolders = $("#passHolders").value();
                         if (passHolders == 0) {
                             //                         $(".otherDiv").each(function (e) {
                             //                             var passengerType = e.attr("passengerType");
                             //                             if (passengerType != "")
                             //                                 e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '220', minWidth: '220' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_title', content: getTitleTips(passengerType)} });
                             //                         });
                         }
                         $(".d_plus").each(function (e) {
                             var tips = e.attr("tips");
                             e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '179', minWidth: '179' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_beyond_day', content: { txt: tips}} });
                         }
                     );
                         //                     $(".refundDiv").each(function (e) {
                         //                         var refund = e.attr("refund");
                         //                         if (refund && refund != '') {
                         //                             e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '280', minWidth: '280' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_Rule', content: getTitleTips(refund)} });
                         //                         }
                         //                     });
                         $(".base_txtdiv").each(function (e) {
                             var refund = e.attr("refund");
                             if (refund && refund != '') {
                                 //e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '280', minWidth: '280' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_Rule', content: getTitleTips(refund)} });
                             }
                             var crefund = e.attr("crefund");
                             if (crefund && crefund != '') {
                                 e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '350', minWidth: '350' }, showArrow: false, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_CRefund', content: getTitleTips(crefund)} });
                             }
                             var erefund = e.attr("erefund");
                             if (erefund && erefund != '') {
                                 e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '350', minWidth: '350' }, showArrow: false, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_CRefund', content: getTitleTips(erefund)} });
                             }
                         });
                         $(".t_blue").each(function (e) {
                             var refund = e.attr("refund");
                             if (refund && refund != '') {
                                 e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '250', minWidth: '250' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_active', content: getTitleTips(refund)} });
                             }

                         });
                         $(".t_red").each(function (e) {
                             var refund = e.attr("refund");
                             if (refund && refund != '') {
                                 e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '250', minWidth: '250' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_active', content: getTitleTips(refund)} });
                             }

                         });
                         $("[name='spActiveTag']").each(function (e) {
                             e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '220', minWidth: '220' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_active', content: getTitleTips("TGV活动:6.15-7.16期间凡预订TGV系列列车，预订成功后分享截图集赞，最高可获得一万元费用报销。<a href='http://pages.ctrip.com/commerce/promote/201506/flight/TGV/index.html' target='_blank' style='color:#06c'>点击查看详情</a>")} });
                         });
                         $("#searchLoading").css("display", "none");


                         isRunning = false;
                         //没有加载满，则继续自动加载
                         if (noResult == 0 && document.getElementById("tbodyProductList").offsetHeight < (getClientHeight() - 350)) {
                             GetPTPProductList();
                         }
                    }

                 },
                 onerror: function () {
                     if ($("#tbodyProductList").html().trim() == "") {
                         $("#divNoResult").css("display", "");
                     }
                     $("#searchLoading").css("display", "none");
                 }
             });

};

var GetPTPTrainTimeList = function (params) {

    isRunning = true;
    $("#searchLoadingTime").css("display", "");
    var value = getParams(params);

    if (LastTimeLow != "") {
        value.departureTimeLow = LastTimeLow;
    }

    var pageStatus = $("#pageStatus").value();
    if (pageStatus == "2") {
        var departureDate = value.departureDate;
        var departureTimeHigh = value.departureTimeHigh;
        var departureTimeLow = value.departureTimeLow;
        var fromCity = value.fromCityCode;
        var toCity = value.toCityCode;
        var arriveDate = value.arriveDate;
        var startCityName = value.startCityName;
        var destCityName = value.destCityName;
        var backTimeHigh = value.backTimeHigh;
        var backTimeLow = value.backTimeLow;

        value.departureDate = arriveDate;
        value.departureTimeHigh = backTimeHigh;
        value.departureTimeLow = backTimeLow;
        value.fromCityCode = toCity;
        value.toCityCode = fromCity;
        value.arriveDate = departureDate;
        value.startCityName = destCityName;
        value.destCityName = startCityName;
        value.backTimeHigh = departureTimeHigh;
        value.backTimeLow = departureTimeLow;

        if (LastBackTimeLow != "") {
            value.departureTimeLow = LastBackTimeLow;
        }

        if ($("#hidData").value() != "") {
            value.one = $("#hidData").value();
            $.cookie.set('hidData', 'first', value.one);

        }
        else {
            value.one = $.cookie.get('hidData', 'first');
            //$("#hidData").value(value.one);
        }
        if ($("#hidFirstData").value() != "") {
            value.data = $("#hidFirstData").value();
            $.cookie.set('hidFirstData', 'first', value.data);
        }
        else {
            value.data = $.cookie.get('hidFirstData', 'first');
        }
        if ($("#hidBookData").value() != "") {
            value.BookData = $("#hidBookData").value();
            if ($("#tbodyProductList").html().trim() == "") {
                $.cookie.set('hidBookData', 'first', value.BookData);
                if (!($.cookie.set('hidBookData', 'first'))) {
                    if (localStorage) {
                        localStorage.setItem('hidBookData', value.BookData);
                    }
                }
            }
        }
        else {
            value.BookData = ($.cookie.get('hidBookData', 'first') == "" || $.cookie.get('hidBookData', 'first') == "undefined") ? (localStorage ? localStorage.getItem('hidBookData') : "") : $.cookie.get('hidBookData', 'first');
        }

    }
    else {
        if ($("#hidBookData").value() != "") {
            value.BookData = $("#hidBookData").value();
        }
    }
    $("#divNoResultTime").css("display", "none");

    cQuery.ajax(applicationAddress + "Ajax/PTPProductListHandler.ashx?Action=GetPTPTrainTimeList",
        {
            method: 'POST',
            timeout: 3000,
            context: 'value=' + $.stringifyJSON(value),
            onsuccess: function (result) {
                isBrowerBack = false;
                var data = cQuery.parseJSON(result.responseText); //强制转换一下json字符串，生成json对象
                if (data != null && data != 'undefined') {
                    noResult = data.NoResult;
                    if (data.LastTimeLow) {
                        LastTimeLow = data.LastTimeLow;
                    }
                    if (data.LastBackTimeLow) {
                        LastBackTimeLow = data.LastBackTimeLow;
                    }
                    if (value.passHolders == 0)//订座
                    {
                        pageid = 103123;
                    }
                    else {//点对点
                        pageid = 103112;
                    }

                    if (data.ShowHtml != "") {
                        $("#tbodyTrainTimeProductList").html($("#tbodyTrainTimeProductList").html() + data.ShowHtml);
                        //$("#tbodyProductList").append(data.ShowHtml);
                        $("#divNoResultTime").css("display", "none");
                    }
                    else {
                        if ($("#tbodyTrainTimeProductList").html().trim() == "") {
                            $("#divNoResultTime").css("display", "");
                            $("#searchLoadingTime").css("display", "none");
                            try {
                                //埋点
                                if (typeof window['__bfi'] == 'undefined') window['__bfi'] = [];
                                window['__bfi'].push(['_tracklog', 'train_outie_list_nonresult_online', "{'uid':'${duid}','page_id':'${page_id}','VERSION':'1','starcity':'" + $("#hdstCode").value() + "','arrivecity':'" + $("#hddtCode").value() + "','starttime':'" + $("#txtDateDep").value() + "','traveltype':'" + $("#MaiDianTravelType").value() + "'}"]);
                            }
                            catch (ex) { }
                        }
                    }

                    //添加pageID
                    $("#page_id").value(pageid);
                    $("#hidBookData").value(data.BookingData);

                    var passHolders = $("#passHolders").value();
                    if (passHolders == 0) {
                        $(".otherDiv").each(function (e) {
                            var passengerType = e.attr("passengerType");
                            if (passengerType != "")
                                e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '220', minWidth: '220' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_title', content: getTitleTips(passengerType)} });
                        });
                    }
                    $(".d_plus").each(function (e) {
                        var tips = e.attr("tips");
                        e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '179', minWidth: '179' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_beyond_day', content: { txt: tips}} });
                    }
                );
                    $(".refundDiv").each(function (e) {
                        var refund = e.attr("refund");
                        e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '280', minWidth: '280' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_Rule', content: getTitleTips(refund)} });
                    });

                    $("[name='spActiveTag']").each(function (e) {
                        e.regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '220', minWidth: '220' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_active', content: getTitleTips("TGV活动:6.15-7.16期间凡预订TGV系列列车，预订成功后分享截图集赞，最高可获得一万元费用报销。<a href='http://pages.ctrip.com/commerce/promote/201506/flight/TGV/index.html' target='_blank' style='color:#06c'>点击查看详情</a>")} });
                    });
                    $("#searchLoadingTime").css("display", "none");


                    isRunning = false;
                    //没有加载满，则继续自动加载
                    //                if (noResult == 0 && document.getElementById("tbodyProductList").offsetHeight < (getClientHeight() - 350)) {
                    //                    GetPTPProductList();
                    //                }
                }
            },
            onerror: function () {
                if ($("#tbodyTrainTimeProductList").html().trim() == "") {
                    $("#divNoResultTime").css("display", "");
                }
                $("#searchLoadingTime").css("display", "none");
            }
        });

};

var GetGoHtml = function () {
    var pageStatus = $("#pageStatus").value();
    if (pageStatus == "2") {
        var data;
        if ($("#hidData").value() != "") {
            data = $("#hidData").value();
            $.cookie.set('hidData', 'first', data);

        }
        else {
            data = $.cookie.get('hidData', 'first');
            $("#hidData").value(data);
        }
        var newObject = $.parseJSON(data);
        newObject.passHolders = requestParameter.PassHolders || global.getQueryStringByName('passHolders');
        cQuery.ajax(applicationAddress + "Ajax/PTPProductListHandler.ashx?Action=GetGoHtml",
           {
               method: 'POST',
               context: 'value=' + $.stringifyJSON(newObject),
               onsuccess: function (result) {
                   var data = result.responseText;
                   $("#transis_id").html(data);
                   $("#goDetails").regMod('jmp', '1.0', { options: { boundaryShow: false, dataUrl: '', css: { maxWidth: '280', minWidth: '280' }, type: 'jmp_title', position: 'bottomLeft-topLeft', classNames: { boxType: 'jmp_title' }, template: '#jmp_Rule', content: getTitleTips($("#goDetails").attr("refund"))} });
               },
               onerror: function (result) {
               }
           });

    }
}

function getTitleTips(str) {
    if (str != '' && str != null) {
        var valueObj = {};

        if (str.indexOf("TGV活动:") == 0) {
            str = str.replace("TGV活动:", "");
            valueObj['content'] = str;
            return valueObj;
        }

        if (str.indexOf("标签详解:") == 0) {
            str = str.replace("标签详解:", "");
            valueObj['content'] = str;
            return valueObj;
        }

        var array = new Array(3);
//        var arr = str.split('|');
//        if (arr != "" && arr != null) {
//            if (str.indexOf("规则") == -1) {
//                if (arr.length == 1) {
//                    str = str + "||";
//                }
//                else if (arr.length == 2) {
//                    str = str + "|";
//                }
//                arr = str.split('|');
//                var IsHavePrice = 'false';
//                for (var i = 0; i < 4; i++) {
//                    if (arr[i] != "") {
//                        var obj = arr[i].split('^');
//                        if (obj[1] == "" || obj[2] == 0) {
//                            valueObj['text' + i] = "";
//                        }
//                        else {
//                            IsHavePrice = 'true';
//                            valueObj['text' + i] = "<li><span class='tipP'><strong>" + obj[0] + "</strong></span>：<dfn>&yen;</dfn><span class='tipPrice'>" + obj[1] + "</span>× " + obj[2] + "</li>";
//                        }
//                    }
//                    else {
//                        valueObj['text' + i] = "";
//                    }
//                }
//                if (IsHavePrice == 'false') {
//                    valueObj['text4'] = "<li><strong>本行程价格明细暂时无法获取</strong></li>";
//                }
//                else {
//                    valueObj['text4'] = "";
//                }
//            }
//            else if (arr != "" && arr != null) {
//                valueObj['title'] = arr[0];
//                valueObj['ruleText'] = arr[1];
//            }
//        }

        var cArrRule = str.split('^');
        if (cArrRule && cArrRule != '' && cArrRule.length>0) {
            valueObj['crule'] = '';
            var segmentNumber = '';
            if (cArrRule[0] != '' && (cArrRule[0] == 'c' || cArrRule[0] == 'e')) {
                for (var c = 0; c < cArrRule.length; c++) {

                    if (parseInt(cArrRule.length, 10) <= 3) {
                        segmentNumber = "";
                    }
                    else {
                        segmentNumber = "<tr><td colspan='2' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'><strong>第" + PTPMyProcess.GetCNNumber(parseInt(c + 1, 10)) + "程</strong></td></tr>";
                    }

                    if (cArrRule[0] != '' && cArrRule[0] == 'c' && cArrRule[c + 1] && cArrRule[c + 1] != '') {
                        if (cArrRule[c + 1].indexOf('|') > 0) {
                            var cArrRuleSeat = cArrRule[c + 1].split('|');
                            if (cArrRuleSeat && cArrRuleSeat.length>1)
                            {
                                var cSeat = cArrRuleSeat[0].split('#');
                                var cSeat2 = cArrRuleSeat[1].split('#');
                                if (cSeat[0] && cSeat[0] != '') {
                                    var saleRule = "";
                                    if (cSeat[5].trim() == cSeat2[5].trim()) {
                                        saleRule = cSeat[5].trim();
                                    }
                                    else {
                                        saleRule = "1.车票： " + cSeat[5] + "<br/>2.订座票：" + cSeat2[5];
                                    }

                                    valueObj['crule'] += "<table style='padding: 0;width: 350px;'><tbody>" + segmentNumber + "<tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top;'>车票类型</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + cSeat[0] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>是否有座</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + cSeat[1] + "</td></tr>"
                    + "<tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>改签</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + cSeat[2] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>退票说明<p style='color:#999'>限未使用</p></td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top;'>1.车票：" + cSeat[3] + "<br/>2.订座票：" + cSeat2[3] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>额外费用</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + cSeat[4] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>使用条件</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + saleRule + "</td></tr></tbody></table>";
                                }
                            }

                        }
                        else {
                            var ccArrRule = cArrRule[c + 1].split('#');
                            if (ccArrRule[0] && ccArrRule[0] != '') {
                                valueObj['crule'] += "<table style='padding: 0;width: 350px;'><tbody>" + segmentNumber + "<tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top;'>车票类型</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + ccArrRule[0] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>是否有座</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + ccArrRule[1] + "</td></tr>"
                    + "<tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>改签</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + ccArrRule[2] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>退票说明<p style='color:#999'>限未使用</p></td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top;'>" + ccArrRule[3] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>额外费用</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + ccArrRule[4] + "</td></tr><tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>使用条件</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'> " + ccArrRule[5] + "</td></tr></tbody></table>";
                            }
                        }
                    }

                    if (cArrRule[0] != '' && cArrRule[0] == 'e' && cArrRule[c + 1] && cArrRule[c + 1] != '') {
                        if (cArrRule[c + 1].indexOf('|') > 0) {
                            var cArrRuleSeat = cArrRule[c + 1].split('|');
                            if (cArrRuleSeat && cArrRuleSeat.length > 1) {
                                var cSeat = cArrRuleSeat[0].split('#');
                                var cSeat2 = cArrRuleSeat[1].split('#');
                                if (cSeat[0] && cSeat[0] != '') {
                                    valueObj['crule'] += "<table style='padding: 0;width: 350px;'><tbody>" + segmentNumber + "<tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>车票类型</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + cSeat[0] + "</td></tr>"
                    + "<tr><td colspan='2' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>购票规则：<br>1.车票：" + cSeat[1] + "<br/>2.订座票：" + cSeat2[1] + "</td></tr><tr><td colspan='2' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>退票规则：<br>1.车票：" + cSeat[2] + "<br/>2.订座票：" + cSeat2[2] + "</td></tr></tbody></table>";
                                }
                            }

                        }
                        else {
                            var ecArrRule = cArrRule[c+1].split('#');
                            if (ecArrRule[0] && ecArrRule[0] != '') {
                                valueObj['crule'] += "<table style='padding: 0;width: 350px;'><tbody>" + segmentNumber + "<tr><td width='20%' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>车票类型</td><td style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>" + ecArrRule[0] + "</td></tr>"
                    + "<tr><td colspan='2' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>购票规则：<br>" + ecArrRule[1] + "</td></tr><tr><td colspan='2' style='border: 1px solid #ccc;padding: 5px;vertical-align: top'>退票规则：<br>" + ecArrRule[2] + "</td></tr></tbody></table>";
                            }
                        }
                    }
                }
            }
        }

        return valueObj;
    }
    return {};
}

var TravelTypeChange = function () {
    var type = $("#selTravelType").value();
    var display = "";
    if (type == 0) {
        display = "none";
    }
    $("#spanBackDate").css("display", display);
    $("#txtDateAri").css("display", display);
    $("#sltAriTime").css("display", display);
    document.getElementById("spanBackDate").style.display = display;
    document.getElementById("txtDateAri").style.display = display;
    document.getElementById("sltAriTime").style.display = display;
}

var ShowMorePrice = function (trainNum, obj) {

    var display = "none";
    var trArray = $("tr[num='" + trainNum + "']");
    if ($(obj).lastChild().hasClass("i_tri_dn")) {
        $(obj).html("收起<i class='i_tri i_tri_up'>");
        display = "";
    }
    else {
        $(obj).html("更多<i class='i_tri i_tri_dn'>");
    }

    trArray.each(function (tr) {
        tr.css("display", display);
    });
    global.preventDefault();
}

var Search = function () {
    try {
        $.pageStorage.clear();
    }
    catch (ex) { }
    //    isBrowerBack = false;
    var checkValue = checkSearchBar(); if (checkValue) {
        if ($("#hdstCode").value().indexOf("TW") != 0) {
            window.location.href = host + address + checkValue;
        }
        else {
            window.location.href = host + "train/" + $("#hdstCode").value() + "-" + $("#hddtCode").value() + "?" + "departureDate=" + $("#trainTxtDateDep").value(); ;
        }
    }
    else
    { return false; }
}

function $type(opt) {

    var op = Object.prototype;
    var ostring = op.toString;

    return isFunction(opt) || isArray(opt);

    function isFunction(it) {
        return ostring.call(it) === '[object Function]';
    }

    function isArray(it) {
        return ostring.call(it) === '[object Array]';
    }

}

function isNull(node) {
    return node.value() === "";
}

function checkSearchBar(opts) {
    var O = { needCheckCity: true,
        needCheckBack: false,
        nodes: { startCity: $("#txtCityDep"),
            startCityHidden: $("#hdstCode"),
            destCity: $("#txtCityAri"),
            destCityHidden: $("#hddtCode"),
            startDate: $("#txtDateDep"),
            trainStartDate: $("#trainTxtDateDep"),
            startTime: $("#sltDepTime"),
            backDate: $("#txtDateAri"),
            backTime: $("#sltAriTime"),
            searchType: $("#selTravelType"),
            pageStatus: $("#pageStatus"),
            passHolders: $("#zuoWeiPassengerNumber"),
            adult: adultsPassengerNumbers + "",
            child: childrenPassengerNumbers + "",
            youth: youthPassengerNumbers + "",
            seniors: elderPassengerNumbers + ""
        },
        message: { startCity: "请选择出发城市", destCity: "请选择到达城市", startDate: "请选择出发日期", startTime: "请选择具体出发时间段",
            backDate: "请选择返程日期", backTime: "请选择具体返回时间段", cityCanotEqual: "您选择的目的城市和出发城市相同，请重新选择",
            dateCheck: "您选择的返回日期早于出发日期，请重新选择", peopleIsZero: "乘客数量不能为0，请输入乘客数量"
        },
        paramName:
            { startCityHidden: "from", startCity: "startCityName", destCity: "destCityName",
                destCityHidden: "to",
                startDate: "departureDate",
                startTime: "starttime", backDate: "arriveDate", backTime: "backtime", searchType: "searchType", pageStatus: "pageStatus", passHolders: "passHolders", adult: "adult", child: "child", youth: "youth", seniors: "seniors"
            }
    };
    function checkNull(nodes) {
        var key, node; for (var i = 0, l = nodes.length; i < l; i++) {
            key = nodes[i]; node = O.nodes[key]; if (node && isNull(node)) {
                validateShow(node, '该填写项不能为空');
                return false;
            }
        }
        return true;
    }
    if (O.nodes["searchType"].value() === "1")
        O.needCheckBack = true;
    if (O.needCheckCity) {
        if (!checkNull(["startCity", "destCity"])) {
            return false;
        }
        if (O.nodes["startCity"].value().trim() === O.nodes["destCity"].value().trim()) {
            validateShow($("#txtCityAri"), '出发城市和到达城市不能相同');
            return false;
        }
        if (O.nodes["startCityHidden"] && isNull(O.nodes["startCityHidden"])) {
            validateShow($("#txtCityDep"), '请重新选择出发城市');
            return false;
        }
        if (O.nodes["destCityHidden"] && isNull(O.nodes["destCityHidden"])) {
            validateShow($("#txtCityAri"), '请重新选择到达城市');
            return false;
        }
    }
    if (!checkNull(["startDate", "startTime"]))
    { return false; }
    if (IsStartCityTW) {
        if (new Date(O.nodes["trainStartDate"].value().trim().replace(/\-/g, '/')) < (new Date().addDays(parseInt(trainAddDaysFrom - 1)))) {
            validateShow(O.nodes["trainStartDate"], '只能预订当前日期' + trainAddDaysFrom + '天之后的车票');
            return false;
        }
    }
    else {
        if (new Date(O.nodes["startDate"].value().trim().replace(/\-/g, '/')) < (new Date().addDays(parseInt(OTStartDate - 1)))) {
            validateShow(O.nodes["startDate"], '只能预订当前日期' + OTStartDate + '天之后的车票');
            return false;
        }
    }

    if (O.needCheckBack) {
        if (!checkNull(["backDate", "backTime"]))
        { return false; }
        var _startDate = O.nodes["startDate"].value().split("-"), _backDate = O.nodes["backDate"].value().split("-"); for (var i = 0; i < 3; i++) {
            _startDate[i] = _startDate[i] * 1; _backDate[i] = _backDate[i] * 1; if (_backDate[i] < _startDate[i]) {
                validateShow($("#txtDateAri"), '返回日期不能小于出发日期');
                //                alert(O.nodes["backDate"], O.message["dateCheck"]);
                return false;
            }
            else if (_backDate[i] > _startDate[i])
            { break; }
        }
    }
    else
    { delete O.paramName["backDate"]; delete O.paramName["backTime"]; }
    var adultsNumber = parseInt(O.nodes['adult']);
    var childsNumber = parseInt(O.nodes['child']);
    var youthsNumber = parseInt(O.nodes['youth']);
    var seniorNumbers = parseInt(O.nodes['seniors']);
    var totalNumbers = adultsNumber + childsNumber + youthsNumber + seniorNumbers;
    var passHolders = parseInt(O.nodes['passHolders'].value());
    if (passHolders == 0 && totalNumbers == 0 && $("#hdstCode").value().indexOf("TW") != 0) {
        validateShow($("#txtPtpNumber"), '预订人数总计不能为0');
        return false;
    }
    var param = [], node, _key = "", _value = ""; for (var key in O.paramName) {
        if (node = O.nodes[key]) {
            _key = O.paramName[key].split(",");
            if (!isNaN(node)) {
                _value = node.split(",");
            }
            else {
                _value = node.value().split(",");
            }
            for (var i = 0, l = _key.length; i < l; i++) {
                if (_key[i] == "from" || _key[i] == "to" || _key[i] == "startCityName" || _key[i] == "destCityName")
                    continue;
                if (_key[i] == 'pageStatus' && _value[i] == '2') {
                    param.push(_key[i] + "=" + "1");
                }
                else {
                    param.push(_key[i] + "=" + _value[i]);
                }
            }
        }
    }

    var queryString;
    //    if (O.nodes["startCity"].value() && O.nodes["destCity"].value()) {
    //        queryString = O.nodes["startCity"].value() + "-" + O.nodes["destCity"].value();
    //        queryString += "/";
    //    }
    if (O.nodes["startCityHidden"].value() && O.nodes["destCityHidden"].value()) {
        queryString = O.nodes["startCityHidden"].value() + "-" + O.nodes["destCityHidden"].value();
        queryString += "?";
    }
    return queryString + param.join("&");
    //return param.join("&");
}

function SortBindAndTrigger() {

    var arrowList = $("table.p2p_list_wrap th i");

    $("table.p2p_list_wrap th a").bind("click", toggleAndTrigger);

    var keyValuePair = { "出发时间": 0, "到达时间": 1, "行驶时长": 2, "价格": 3 };

    function toggleAndTrigger() {

        var a = $(this).nextSibling("i");

        arrowList.each(function (a) {
            $(a).attr("checkStatus", "unchecked");
        });

        a.attr("checkStatus", "checked");
        $.event.trigger("broadCast");
        arrowList.each(function (b) {
            var a = $(b);
            if ((a.attr("checkStatus")) == "unchecked") {
                if (a.hasClass("i_listarr_up")) {
                    a.removeClass("i_listarr_up").addClass("i_arrow_up");
                }
                else if (a.hasClass("i_listarr_dn")) {
                    a.removeClass("i_listarr_dn").addClass("i_arrow_up");
                }
            }
        });
        value = keyValuePair[$(this).text()];
        if (a.hasClass("i_listarr_up")) {
            a.removeClass("i_listarr_up").addClass("i_listarr_dn");
            sortData(value, "dn");

        }
        else if (a.hasClass("i_listarr_dn")) {
            a.removeClass("i_listarr_dn").addClass("i_listarr_up");
            sortData(value, "up");
        }
        else if (a.hasClass("i_arrow_up")) {
            a.removeClass("i_arrow_up").addClass("i_listarr_up");
            sortData(value, "up");
        }
        else if (a.hasClass("i_arrow_dn")) {
            a.removeClass("i_arrow_dn").addClass("i_listarr_dn");
            sortData(value, "dn");
        }

    }

    function sortData(index, order) {
        var tb = $("#tbodyProductList").childNodes();
        var total = tb.length;
        //外层循环，共要进行arr.length次求最大值操作
        //wyh 暂时更改为从1开始
        for (var i = 0; i < total - 1; i++) {
            if (tb[i].nodeName.toLowerCase() !== "tr")
                continue;
            if (!($(tb[i]).attr("sort")))
                continue;
            //内层循环，找到第i大的元素，并将其和第i个元素交换
            for (var j = i; j < total; j++) {
                if (tb[j].nodeName.toLowerCase() !== "tr")
                    continue;
                if (!($(tb[j]).attr("sort"))) {
                    continue;
                }
                var data1 = $(tb[i]).attr("sort").split("|")[index];
                var data2 = $(tb[j]).attr("sort").split("|")[index];
                var v;
                var v2;
                if (index == 0 || index == 1) {
                    if (timeCompare(data1, data2, order)) {
                        swapRow(i, j);
                        tb = $("#tbodyProductList").childNodes();
                    }
                }
                else {
                    if (priceCompare(data1, data2, order)) {
                        swapRow(i, j);
                        tb = $("#tbodyProductList").childNodes();
                    }
                }
            }
        }
        return;
    }

    function priceCompare(data1, data2, order) {
        var value1 = parseInt(data1);
        var value2 = parseInt(data2);
        if (order == "up") {
            if (value1 > value2)
                return true;
            else
                return false;
        }
        else if (order == "dn") {
            if (value1 < value2)
                return true;
            else
                return false;
        }
    }

    function swapRow(i, k) {
        var tb = $("#tbodyProductList").childNodes();
        $(tb[k]).insertBefore($(tb[i]));
        $(tb[i]).insertAfter($(tb[k]));
    }

    function timeCompare(data1, data2, order) {
        {
            var array1 = data1.split(":");
            var array2 = data2.split(":");
            var timeObject1 = { hour: array1[0], minute: array1[1] };
            var timeObject2 = { hour: array2[0], minute: array2[1] };
            if (order == "up") {
                if (timeObject1.hour < timeObject2.hour) {
                    return false;
                }
                else if (timeObject1.hour === timeObject2.hour) {
                    if (timeObject1.minute < timeObject2.minute) {
                        return false;
                    }
                    else if (timeObject1.minute == timeObject2.minute) {
                        return true;
                    }
                    else {
                        return true;
                    }
                }
                else {
                    return true;
                }
            }
            else if (order == "dn") {
                if (timeObject1.hour < timeObject2.hour) {
                    return true;
                }
                else if (timeObject1.hour === timeObject2.hour) {
                    if (timeObject1.minute < timeObject2.minute) {
                        return true;
                    }
                    else if (timeObject1.minute == timeObject2.minute) {
                        return false;
                    }
                    else {
                        return false;
                    }
                }
                else {
                    return false;
                }
            }
        }


    }
}

function showGrade(fnName) {
    var iTop = (window.screen.height - 30 - 720) / 2; //获得窗口的垂直位置;
    var iLeft = (window.screen.width - 10 - 865) / 2; //获得窗口的水平位置;
    window.open(applicationAddress + fnName, 'newwindow', 'height=720, width=865, top=' + iTop + ', left=' + iLeft + ', toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no', "_blank");
}

//SSO_Booking回调
function __SSO_submit(a, t) {
    BookingBtnClickCallBack(a);
}

//回调函数
var BookingBtnClickCallBack = function (a) {
    var local = a;
    var pageStatus = $("#pageStatus").value();
    var passHolders = $("#passHolders").value();
    var id = $(local).attr("PkgID");
    var array = [];
    var hidStr = $(local).nextSibling();
    if (hidStr) {
        array.push("hidPostData" + "$" + $(hidStr).value());
    }

    var bookData = cQuery.parseJSON($("#hidBookData").value())
    var goData, backData;
    if (pageStatus == "0") {
        for (var i = 0; i < bookData.length; i++) {
            if (bookData[i].PackagePrices.PackageFareId == id) {
                array.push("hidGoData" + "$" + cQuery.stringifyJSON(bookData[i]));
            }
        }
    }
    else {
        for (var i = 0; i < bookData.length; i++) {
            if (bookData[i].WayType == "1") {
                array.push("hidGoData" + "$" + cQuery.stringifyJSON(bookData[i]));
            }
            else if (bookData[i].PackagePrices.PackageFareId == id && bookData[i].WayType == "2") {
                array.push("hidBackData" + "$" + cQuery.stringifyJSON(bookData[i]));
            }
        }
    }
    array.push("requestParameter$" + $("#requestParameter").value());
    var passHolders = requestParameter.PassHolders || global.getQueryStringByName('passHolders');
    if (passHolders == "0") {
        array.push("orderType$1"); //点对点订票标志
        //array.push("passengerType$" + "adult=" + $("#dropAdult").value() + "|child=" + $("#dropChild").value() + "|youth=" + $("#dropYouth").value() + "|seniors=" + $("#dropSeniors").value());
        array.push("passengerType$" + "adult=" + dropAdult + "|child=" + dropChild + "|youth=" + dropYouth + "|seniors=" + dropSeniors);
    }
    else {
        array.push("orderType$2"); //座位订票标志
        var zuoweiNumbers = $("#zuoWeiPassengerNumber").value();
        array.push("zuoweiSelected$" + zuoweiNumbers);
    }
    StandardPost(host + "otinput", array);
}

function StandardPost(url, args) {
    //    var form = document.createElement("FORM");
    //    form.method = "POST";
    document.forms[0].action = url;
    //    form.id = "formInput";
    for (var i = 0; i < args.length; i++) {
        var array = Array;
        array = args[i].split('$');
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = array[0];
        input.id = array[0];
        input.value = array[1];
        $(document.forms[0]).append($(input));
    }

    document.forms[0].submit();
}


//获取滚动条当前的位置
function getScrollTop() {
    var scrollTop = 0;
    if (document.documentElement && document.documentElement.scrollTop) {
        scrollTop = document.documentElement.scrollTop;
    }
    else if (document.body) {
        scrollTop = document.body.scrollTop;
    }
    return scrollTop;
}

//获取当前可视范围的高度
function getClientHeight() {
    var clientHeight = 0;
    if (document.body.clientHeight && document.documentElement.clientHeight) {
        clientHeight = Math.min(document.body.clientHeight, document.documentElement.clientHeight);
    }
    else {
        clientHeight = Math.max(document.body.clientHeight, document.documentElement.clientHeight);
    }
    return clientHeight;
}

//获取文档完整的高度
function getScrollHeight() {
    return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
}

function CheckStartCity() {
    var display = "";

    if ($("#hdstCode").value().indexOf("TW") == 0) {
        display = "none";
        IsStartCityTW = true;
        TravelTypeChange();
        PTPMyProcess.DefaultTraveType();
    }
    else {
        IsStartCityTW = false;
    }

    $("#divPassengerNumber,#spanBackDate,#sltAriTime,.fr,.tk_hd_info,#sltDepTime,#txtDateAri,#bTimeTxt,#dTimeTxt,#bDateli").css("display", display);

    if (IsStartCityTW) {
        //台湾城市
        $("#trainTxtDateDep").css("display", "");
        $("#txtDateDep").css("display", "none");
        var strdeDate = $("#txtDateDep").value().trim().replace(/\-/g, '/');
        var dtdeDate = new Date(strdeDate);
        var now = new Date(new Date().toDateString());
        if (dtdeDate > now.addDays(trainAddDaysTo)) {
            $("#trainTxtDateDep").value(now.addDays(trainAddDaysTo).toFormatString("yyyy-MM-dd"));
        } else if (dtdeDate > now.addDays(trainAddDaysFrom)) {
            $("#trainTxtDateDep").value(dtdeDate.toFormatString("yyyy-MM-dd"));
        } else {
            $("#trainTxtDateDep").value(now.addDays(trainAddDaysFrom).toFormatString("yyyy-MM-dd"));
        }

    }
    else {
        //非台湾城市
        $("#trainTxtDateDep").css("display", "none");
        $("#txtDateDep").css("display", "");
        var strdeDate = $("#trainTxtDateDep").value().trim().replace(/\-/g, '/');
        var dtdeDate = new Date(strdeDate);
        var now = new Date(new Date().toDateString());
        if (dtdeDate < now.addDays(OTStartDate)) {
            $("#txtDateDep").value(now.addDays(OTDefaultStartDate).toFormatString("yyyy-MM-dd"));
        } else {
            $("#txtDateDep").value(dtdeDate.toFormatString("yyyy-MM-dd"));
        }

    }
}

//js方法
var PTPMyProcess = {
    Init: function () {
        $("#txtPtpNumber").bind("click", PTPMyProcess.choosePassengerNumber);
        $("#mainbody").bind("click", PTPMyProcess.hidePtpSelectNumber);
        $("#dropPassHolders").bind("click", PTPMyProcess.chooseZuoWeiPassengerNumber);
        $("#change").bind("click", PTPMyProcess.ChangeCity);
        $("#txtDateAri").bind("change", PTPMyProcess.changeStatus);
        $("#dTimeTxt").bind("click", function () { PTPMyProcess.DepTimePro("ddlTime"); });
        $("#dTimeTxt").bind("mouseover", function () { depTimeisOut = false; });
        $("#dTimeTxt").bind("mouseout", function () { depTimeisOut = true; });
        $("#ddlTime").bind("mouseover", function () { depTimeisOut = false; });
        $("#ddlTime").bind("mouseout", function () { depTimeisOut = true; });
        $("#dhours").bind("click", function (obj) { PTPMyProcess.GetTimeData(1, 1, obj); });
        $("#dminutes").bind("click", function (obj) { PTPMyProcess.GetTimeData(2, 1, obj); });
        $("#bTimeTxt").bind("click", function () { PTPMyProcess.DepTimePro("bdlTime"); });

        $("#bTimeTxt").bind("mouseover", function () { backTimeisOut = false; });
        $("#bTimeTxt").bind("mouseout", function () { backTimeisOut = true; });
        $("#bdlTime").bind("mouseover", function () { backTimeisOut = false; });
        $("#bdlTime").bind("mouseout", function () { backTimeisOut = true; });
        $("#bhours").bind("click", function (obj) { PTPMyProcess.GetTimeData(1, 2, obj); });
        $("#bminutes").bind("click", function (obj) { PTPMyProcess.GetTimeData(2, 2, obj); });


    },
    GetCNNumber: function (obj) {
        if (parseInt(obj, 10) == 1) {
            return "一";
        }
        else if (parseInt(obj, 10) == 2) {
            return "二";
        }
        else if (parseInt(obj, 10) == 3) {
            return "三";
        }
        else if (parseInt(obj, 10) == 4) {
            return "四";
        }
        else if (parseInt(obj, 10) == 5) {
            return "五";
        }
        else if (parseInt(obj, 10) == 6) {
            return "六";
        }
        else if (parseInt(obj, 10) == 7) {
            return "七";
        }
        else if (parseInt(obj, 10) == 8) {
            return "八";
        }
        else if (parseInt(obj, 10) == 9) {
            return "九";
        }
    },
    Show: function (obj) {
        $("#" + obj).css("display", "");
    },
    Hide: function (obj) {
        $("#" + obj).css("display", "none");
    },
    MyTrigger: function (id) {
        var numberDisplay = document.getElementById(id).style.display;
        if (numberDisplay != "none") {
            document.getElementById(id).style.display = "none";
            $("#" + id).css("display", "none");
            if (id == 'ddlTime') {
                depTimeIsShow = 0;
            }
            else if (id == 'bdlTime') {
                backTimeIsShow = 0;
            }
        }
        else {
            $("#" + id).css("display", "");
            document.getElementById(id).style.display = "";
        }
    },
    choosePassengerNumber: function () {
        PTPMyProcess.MyTrigger("ptpSelectNumber");
    },
    hidePtpSelectNumber: function () {
        if (isOut && document.getElementById("ptpSelectNumber").style.display != "none") {
            document.getElementById("ptpSelectNumber").style.display = "none";
        }
        if (zuoweiisOut && document.getElementById("zuoWeiSelectNumber").style.display != "none") {
            document.getElementById("zuoWeiSelectNumber").style.display = "none";
        }
        if (traveTypeisOut && document.getElementById("ulTraveType").style.display != "none") {
            document.getElementById("ulTraveType").style.display = "none";
        }
        if (depTimeisOut && document.getElementById("ddlTime").style.display != "none") {
            document.getElementById("ddlTime").style.display = "none";
            depTimeIsShow = 0;
        }
        if (backTimeisOut && document.getElementById("bdlTime").style.display != "none") {
            document.getElementById("bdlTime").style.display = "none";
            backTimeIsShow = 0;
        }
    },
    //乘客人数处理
    ProPassengerNumber: function (index, type) {
        if (type == 'c')//减少乘客
        {
            if ($("#passengerNumber" + index).value() != '' && parseInt($("#passengerNumber" + index).value()) > 0) {
                $("#passengerNumber" + index).value(parseInt($("#passengerNumber" + index).value()) - 1);
                PTPMyProcess.SetPassengerNumber(index, $("#passengerNumber" + index).value());
            }
        }
        else if (type == 'a')//添加乘客
        {
            if ($("#passengerNumber" + index).value() != '' && parseInt($("#passengerNumber" + index).value()) < parseInt(totalNumbers) && parseInt(totalNumbers) > parseInt(parseInt(adultsPassengerNumbers) + parseInt(childrenPassengerNumbers) + parseInt(youthPassengerNumbers) + parseInt(elderPassengerNumbers))) {
                $("#passengerNumber" + index).value(parseInt($("#passengerNumber" + index).value()) + 1);
                PTPMyProcess.SetPassengerNumber(index, $("#passengerNumber" + index).value());
            }
        }

        PTPMyProcess.ProShowPassengerNumber();
    },
    SetPassengerNumber: function (index, value) {
        if (index == 1) {
            childrenPassengerNumbers = value;
        }
        else if (index == 2) {
            youthPassengerNumbers = value;
        }
        else if (index == 3) {
            adultsPassengerNumbers = value;
        }
        else if (index == 4) {
            elderPassengerNumbers = value;
        }
    },
    ProShowPassengerNumber: function () {
        var nowAllPassengerNumber = parseInt(adultsPassengerNumbers) + parseInt(childrenPassengerNumbers) + parseInt(youthPassengerNumbers) + parseInt(elderPassengerNumbers);
        for (var index = 1; index <= 4; index++) {

            if (parseInt(nowAllPassengerNumber) >= parseInt(totalNumbers)) {
                if (!$("#passengerNumber" + index + "a").hasClass("disable")) {
                    $("#passengerNumber" + index + "a").addClass("disable");
                }
            }
            else {
                if ($("#passengerNumber" + index + "a").hasClass("disable")) {
                    $("#passengerNumber" + index + "a").removeClass("disable");
                }
            }
            if (parseInt($("#passengerNumber" + index).value()) > 0 && $("#passengerNumber" + index + "c").hasClass("disable")) {
                $("#passengerNumber" + index + "c").removeClass("disable");
            }
            else if (parseInt($("#passengerNumber" + index).value()) == 0 && !$("#passengerNumber" + index + "c").hasClass("disable")) {
                $("#passengerNumber" + index + "c").addClass("disable");
            }

        }

        if (parseInt(childrenPassengerNumbers) != parseInt($("#passengerNumber1").value())) {
            childrenPassengerNumbers = $("#passengerNumber1").value();
        }
        if (parseInt(youthPassengerNumbers) != parseInt($("#passengerNumber2").value())) {
            youthPassengerNumbers = $("#passengerNumber2").value();
        }
        if (parseInt(adultsPassengerNumbers) != parseInt($("#passengerNumber3").value())) {
            adultsPassengerNumbers = $("#passengerNumber3").value();
        }
        if (parseInt(elderPassengerNumbers) != parseInt($("#passengerNumber4").value())) {
            elderPassengerNumbers = $("#passengerNumber4").value();
        }

        $("#txtPtpNumber").value("");
        if (parseInt(adultsPassengerNumbers) > 0) {
            $("#txtPtpNumber").value(adultsPassengerNumbers + "成人 ");
        }
        if (parseInt(childrenPassengerNumbers) > 0) {
            $("#txtPtpNumber").value($("#txtPtpNumber").value() + childrenPassengerNumbers + "儿童 ");
        }
        if (parseInt(youthPassengerNumbers) > 0) {
            $("#txtPtpNumber").value($("#txtPtpNumber").value() + youthPassengerNumbers + "青年 ");
        }
        if (parseInt(elderPassengerNumbers) > 0) {
            $("#txtPtpNumber").value($("#txtPtpNumber").value() + elderPassengerNumbers + "长者 ");
        }
    },
    chooseZuoWeiNumber: function (obj) {
        $("#dropPassHolders").value($(obj).html().trim());
        $("#zuoWeiPassengerNumber").value($(obj).html().trim());
        document.getElementById("dropPassHolders").value = $(obj).html().trim();
        if (document.getElementById("zuoWeiSelectNumber").style.display != "none") {
            document.getElementById("zuoWeiSelectNumber").style.display = "none";
        }
    },
    chooseZuoWeiPassengerNumber: function () {
        PTPMyProcess.MyTrigger("zuoWeiSelectNumber");
    },
    ChangeCity: function () {
        var startCityName = $("#txtCityDep").value();
        var hidstartCityName = $("#hdstName").value();
        var hidstartCityCode = $("#hdstCode").value();
        var toCityName = $("#txtCityAri").value();
        var hidtoCityName = $("#hddtName").value();
        var hidtoCityCode = $("#hddtCode").value();
        $("#txtCityDep").value(toCityName);
        $("#hdstName").value(hidtoCityName);
        $("#hdstCode").value(hidtoCityCode);
        $("#txtCityAri").value(startCityName);
        $("#hddtName").value(hidstartCityName);
        $("#hddtCode").value(hidstartCityCode);
        CheckStartCity(global);
    },
    changeStatus: function (event) {
        var elementId = (event.target.id == null || event.target.id == 'undefined') ? this.id : event.target.id;
        var span = event.target.previousSibling;
        if (elementId == "txtDateAri") {
            //往返
            if ($($("#txtDateAri").parentNode()).hasClass("disabled")) {
                $($("#txtDateAri").parentNode()).removeClass("disabled");
            }
            PTPMyProcess.ChooseTraveType(1);

        }
    },
    DefaultTraveType: function () {
        if (IsStartCityTW) {
            $("#selTravelType").value(0);
            $("#traveTypeText").html("单程");
        }
    },
    ChooseTraveType: function (obj) {
        if (IsStartCityTW) {
            return false;
        }
        if (obj == 2) {
            PTPMyProcess.Show("ulTraveType");
        }
        else if (obj == 0 || obj == 1) {
            $("#selTravelType").value(obj);
            PTPMyProcess.Hide("ulTraveType");
            if (obj == 0) {
                $("#traveTypeText").html("单程");
                if (!$($("#txtDateAri").parentNode()).hasClass("disabled")) {
                    $($("#txtDateAri").parentNode()).addClass("disabled");
                }
            }
            else if (obj == 1) {
                $("#traveTypeText").html("往返");
                if ($($("#txtDateAri").parentNode()).hasClass("disabled")) {
                    $($("#txtDateAri").parentNode()).removeClass("disabled");
                }
            }
        }

    },
    DepTimePro: function (obj) {
        PTPMyProcess.MyTrigger(obj);
        if (obj == 'ddlTime') {
            var depTime = $("#dTimeTxt").value().trim();
            if (depTime != null && depTime != '') {
                var depTimeArr = depTime.split(':');
                $("#ddlTime li").each(function (obj) { if (obj.hasClass("current")) { obj.removeClass("current"); } });
                $("#dhours li").each(function (obj) {
                    if (depTimeArr[0].trim() == obj.html().trim()) { obj.addClass("current"); }
                    //设置位置
                    document.getElementById("dhours").scrollTop = parseInt((parseInt(depTimeArr[0].trim(), 10) - 2)) * 25;
                });
                $("#dminutes li").each(function (obj) { if (depTimeArr[1].trim() == obj.html().trim()) { obj.addClass("current"); } });
            }
        }
        else if (obj == 'bdlTime') {
            var depTime = $("#bTimeTxt").value().trim();
            if (depTime != null && depTime != '') {
                var depTimeArr = depTime.split(':');
                $("#bdlTime li").each(function (obj) { if (obj.hasClass("current")) { obj.removeClass("current"); } });
                $("#bhours li").each(function (obj) {
                    if (depTimeArr[0].trim() == obj.html().trim()) { obj.addClass("current"); }
                    //设置位置
                    document.getElementById("bhours").scrollTop = parseInt((parseInt(depTimeArr[0].trim(), 10) - 2)) * 25;
                });
                $("#bminutes li").each(function (obj) { if (depTimeArr[1].trim() == obj.html().trim()) { obj.addClass("current"); } });
            }
        }
    },
    ProTimeIsShow: function (type) {
        if (type == 1) {
            if (depTimeIsShow == 0) {
                depTimeIsShow = 1;
            }
            else if (depTimeIsShow == 1) {
                depTimeIsShow = 0;
                PTPMyProcess.Hide("ddlTime");
            }
        }
        else if (type == 2) {
            if (backTimeIsShow == 0) {
                backTimeIsShow = 1;
            }
            else if (backTimeIsShow == 1) {
                backTimeIsShow = 0;
                PTPMyProcess.Hide("bdlTime");
            }
        }
    },
    GetTimeData: function (type, dep, e) {
        var e = e || window.event;
        var obj = e.target || e.srcElement;
        var hmData = $(obj).html().trim();
        if (isNaN(parseInt(hmData, 10))) {
            return false;
        }

        if (type == 1) {//小时

            if (dep == 1)//出发时间
            {
                var depTime = $("#dTimeTxt").value().trim();
                if (depTime != null && depTime != '') {
                    var depTimeArr = depTime.split(':');
                    $("#dTimeTxt").value(hmData + ":" + depTimeArr[1]);
                    $("#sltDepTime").value($("#dTimeTxt").value().trim() + "-24:00");
                    $("#dhours li").each(function (obj) { if (obj.hasClass("current")) { obj.removeClass("current"); } });
                    $(obj).addClass("current");
                }
                PTPMyProcess.ProTimeIsShow(1);
            }
            else if (dep == 2)//到达时间
            {
                var bTime = $("#bTimeTxt").value().trim();
                if (bTime != null && bTime != '') {
                    var bTimeArr = bTime.split(':');
                    $("#bTimeTxt").value(hmData + ":" + bTimeArr[1]);
                    $("#sltAriTime").value($("#bTimeTxt").value().trim() + "-24:00");
                    $("#bhours li").each(function (obj) { if (obj.hasClass("current")) { obj.removeClass("current"); } });
                    $(obj).addClass("current");
                }
                PTPMyProcess.ProTimeIsShow(2);
            }
        }
        else if (type == 2) {//分钟
            if (dep == 1)//出发时间
            {
                var depTime = $("#dTimeTxt").value().trim();
                if (depTime != null && depTime != '') {
                    var depTimeArr = depTime.split(':');
                    $("#dTimeTxt").value(depTimeArr[0] + ":" + hmData);
                    $("#sltDepTime").value($("#dTimeTxt").value().trim() + "-24:00");
                    $("#dminutes li").each(function (obj) { if (obj.hasClass("current")) { obj.removeClass("current"); } });
                    $(obj).addClass("current");
                }
                PTPMyProcess.ProTimeIsShow(1);
            }
            else if (dep == 2)//到达时间
            {
                var bTime = $("#bTimeTxt").value().trim();
                if (bTime != null && bTime != '') {
                    var bTimeArr = bTime.split(':');
                    $("#bTimeTxt").value(bTimeArr[0] + ":" + hmData);
                    $("#sltAriTime").value($("#bTimeTxt").value().trim() + "-24:00");
                    $("#bminutes li").each(function (obj) { if (obj.hasClass("current")) { obj.removeClass("current"); } });
                    $(obj).addClass("current");
                }
                PTPMyProcess.ProTimeIsShow(2);
            }
        }
    },
    ShowMoreSegment: function (trainNum, oarrTime, oarrName, ohours, zarrTime, zarrName, zhours, isAddDays, endAddDays, firstTrainNumber, allTrainNumber, obj) {
        var display = "none";
        var trArray = $("tr[segment='" + trainNum + "']");
        if ($(obj).lastChild().hasClass("i_tri_dn")) {
            $(obj).html("换乘详情<i class='i_tri i_tri_up'>");
            display = "";

            if ($("#pic" + trainNum).hasClass("transfer")) {
                $("#pic" + trainNum).removeClass("transfer");
            }
            try {

                $("#arrName" + trainNum).html(oarrName.trim());
                $("#arrTime" + trainNum).html(oarrTime.trim());
                $("#hours" + trainNum).html(ohours.trim());
                $("#checi" + trainNum).html(firstTrainNumber);
                $("#checi" + trainNum).attr("title", firstTrainNumber);
            } catch (ex) {
                $("#arrTime" + trainNum).innerHTML(oarrTime);
                $("#arrName" + trainNum).innerHTML(oarrName);
                $("#hours" + trainNum).innerHTML(ohours);
            }

            if (parseInt(isAddDays, 10) == 1) {
                $("#addDays" + trainNum).css("display", "");
            }
            if (parseInt(endAddDays, 10) == 1) {
                $("#endAddDays" + trainNum).css("display", "none");
            }
        }
        else {
            $(obj).html("换乘详情<i class='i_tri i_tri_dn'>");
            if (!$("#pic" + trainNum).hasClass("transfer")) {
                $("#pic" + trainNum).addClass("transfer");
            }

            try {
                $("#arrTime" + trainNum).html(zarrTime.trim());
                $("#arrName" + trainNum).html(zarrName.trim());
                $("#hours" + trainNum).html(zhours.trim());
                $("#checi" + trainNum).html(allTrainNumber);
                $("#checi" + trainNum).attr("title", allTrainNumber);
            } catch (ex) {
                $("#arrTime" + trainNum).innerHTML(zarrTime);
                $("#arrName" + trainNum).innerHTML(zarrName);
                $("#hours" + trainNum).innerHTML(zhours);
            }
            if (parseInt(isAddDays, 10) == 1) {
                $("#addDays" + trainNum).css("display", "none");
            }
            if (parseInt(endAddDays, 10) == 1) {
                $("#endAddDays" + trainNum).css("display", "");
            }

        }

        trArray.each(function (tr) {
            tr.css("display", display);
        });
        global.preventDefault();
    },
    ShowValidateCode: function () {
        var isValidateCode = document.getElementById("IsNeedValidateCode").value;
        $("#nextValidateCode").bind("click", function (obj) { PTPMyProcess.NextValidateCode(); });
        $("#btnCode").bind("click", function (obj) { PTPMyProcess.ValidateUserCode(); });
        if (parseInt(isValidateCode, 10) > 0) {
            IsLoadPage = 1;
            $("#validateCode").mask();
            $("#validateCode").css('display', '');
        }
    },
    NextValidateCode: function () {
        var src = $('#imgcode').attr('src') + '&';
        $("#imgcode").attr('src', src);
    },
    ValidateUserCode: function () {
        var code = document.getElementById("userValidateCode").value;
        if (code != "") {
            cQuery.ajax(applicationAddress + "Ajax/ValidateCode.aspx?code=" + code,
             {
                 method: 'POST',
                 timeout: 3000,
                 onsuccess: function (result) {
                     if (result.responseText == "1") {
                         $("#validateCode").css('display', 'none');
                         $("#validateCode").unmask();
                         LoadInit();
                     }
                     else {
                         alert("输入验证码错误！");
                         document.getElementById("userValidateCode").value = "";
                         return false;
                     }
                 },
                 onerror: function () {
                     alert("输入验证码错误！");
                     document.getElementById("userValidateCode").value = "";
                     return false;
                 }
             });
        }
        else {
            alert("验证码不能为空！");
            return false;
        }
    }

};


