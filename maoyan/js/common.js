u = function () {
    var d = "GET",
        c = 40011,
        e = undefined,
        _ = void 0 === e ? 1 : e,
        t = Math.ceil(10 * Math.random()),
        a = (new Date()).getTime(),
        i = typeof window !== "undefined" &&
            window[navigator],
        o = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        u = "method=" + d.toUpperCase() + "&timeStamp=" + a + "&User-Agent=" + o + '&index=' + t + "&channelId=" + c + "&sVersion=" + _,
        f = "&key=A013F70DB97834C0A5492378BD76C53A";
    return {
        timeStamp: a,
        index: t,
        channelId: c,
        sVersion: _,
        signKey:u+f     //调用该值以后还需要进行MD5加密
    }
}
