/* =========================================================
   东华大学一站式学生服务大厅 · 站点脚本
   所有内容由 data/ 下 JSON 驱动，改数据文件即更新
   ========================================================= */
(function(){
  "use strict";
  var $  = function(s, el){ return (el||document).querySelector(s); };
  var $$ = function(s, el){ return Array.prototype.slice.call((el||document).querySelectorAll(s)); };

  var PAGE = document.body.getAttribute("data-page") || "";
  var NAV  = document.body.getAttribute("data-nav") || "";

  function loadJSON(path){
    return fetch(path).then(function(r){
      if(!r.ok){ throw new Error(path + " -> HTTP " + r.status); }
      return r.json();
    });
  }
  function esc(s){
    return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }
  function todayDateStr(){
    var n = new Date();
    return n.getFullYear() + "-" + String(n.getMonth()+1).padStart(2,"0") + "-" + String(n.getDate()).padStart(2,"0");
  }
  function todayKey(){
    var map = {0:"sun",1:"mon",2:"tue",3:"wed",4:"thu",5:"fri",6:"sat"};
    return map[new Date().getDay()];
  }
  function dayLabelCN(k){
    return {mon:"周一",tue:"周二",wed:"周三",thu:"周四",fri:"周五",sat:"周六",sun:"周日"}[k] || k;
  }

  /* ---------- 导航：高亮当前项 + 移动端菜单 ---------- */
  function initNav(){
    $$(".nav-links a").forEach(function(a){
      if(a.getAttribute("data-nav") === NAV){ a.classList.add("active"); }
    });
    var toggle = $(".nav-toggle");
    if(toggle){
      toggle.addEventListener("click", function(){
        $(".nav-links").classList.toggle("open");
      });
    }
  }

  /* ---------- 页脚：站点信息 + 常用链接 ---------- */
  function renderFooter(s){
    var el = $("#foot-site");
    if(el){
      el.textContent = s.siteName + " · " + s.shortName;
    }
    var footLinks = $("#foot-links");
    if(footLinks){
      footLinks.innerHTML = "";
      (s.links||[]).forEach(function(l){
        var a = document.createElement("a");
        a.href = l.url; a.target = "_blank"; a.rel = "noopener";
        a.textContent = l.name;
        footLinks.appendChild(a);
      });
    }
    var footMeta = $("#foot-meta");
    if(footMeta){
      var html = esc(s.address) + "<br>工作时间：" + esc(s.hours) + "<br>邮箱：" + esc(s.email);
      if(s.officialAccount){ html += "<br>微信公众号：" + esc(s.officialAccount); }
      footMeta.innerHTML = html;
    }
  }

  /* ---------- 今日值班状态 ---------- */
  function computeStatus(sched){
    var dateStr = todayDateStr();
    var exc = (sched.exceptions||[]).filter(function(e){ return e.date === dateStr; })[0];
    if(exc){
      if(exc.type === "暂停"){ return {state:"closed", note:exc.note||"今日全体暂停值班"}; }
      return {state:"partial", counters:exc.counters||[], note:exc.note||"部分柜台空班"};
    }
    var base = (sched.weekly||{})[todayKey()] || "休息";
    if(base === "值班"){ return {state:"open", note:""}; }
    return {state:"rest", note:""};
  }

  function renderStatusBanner(sched){
    var box = $("#status-banner") || $("#today-banner");
    if(!box){ return; }
    var st = computeStatus(sched);
    var names = sched.counterNames || {};
    var cls, title, badges = "", extra = "";
    if(st.state === "open"){
      cls = "is-open"; title = "今日正常值班";
      extra = esc(sched.hours || "周一至周五 10:00-19:00（法定节假日除外）");
    }else if(st.state === "partial"){
      cls = "is-partial"; title = "今日部分柜台空班";
      extra = esc(st.note || "");
      st.counters.forEach(function(c){
        badges += '<span class="badge warn">' + esc(names[c]||c) + '</span>';
      });
    }else if(st.state === "closed"){
      cls = "is-closed"; title = "今日暂停值班";
      extra = esc(st.note || "请留意通知公告");
    }else{
      cls = "is-closed"; title = "今日休息";
      extra = "周六、周日大厅不值班，周一至周五 10:00-19:00 正常服务";
    }
    box.className = "status-banner " + cls;
    box.innerHTML =
      '<span class="dot"></span>' +
      '<div><h3>' + esc(title) + '</h3><p>' + extra + '</p>' +
      (badges ? '<div class="badges">' + badges + '</div>' : "") + '</div>';
  }

  /* =========================================================
     页面：首页
     ========================================================= */
  function renderHome(s, sched, notices, counters){
    var bannerEl = $("#status-banner");
    if(bannerEl){ renderStatusBanner(sched); }

    /* 置顶重要通知（最多3条） */
    var list = $("#home-notices");
    if(list){
      var hot = (notices||[]).filter(function(n){ return n.tag === "重要"; })
                            .slice(0,3);
      if(hot.length === 0){
        list.innerHTML = '<div class="empty">暂无重要通知。管理员在 <code>data/notices.json</code> 中把某条通知的 tag 设为“重要”后，会自动置顶显示在首页。</div>';
      }else{
        list.innerHTML = "";
        hot.forEach(function(n){
          var item = document.createElement("div");
          item.className = "notice-item";
          var linkHtml = "";
          if(n.link){
            linkHtml = '<a class="n-link" href="' + esc(n.link) + '" target="_blank" rel="noopener">' + esc(n.linkText||"查看原文") + ' →</a>';
          }
          item.innerHTML =
            '<div class="n-head"><span class="n-title">' + esc(n.title) + '</span>' +
            '<span class="tag hot">置顶</span><span class="n-date">' + esc(n.date) + '</span></div>' +
            (n.body ? '<p class="n-body">' + esc(n.body) + '</p>' : "") + linkHtml;
          list.appendChild(item);
        });
      }
    }

    /* 柜台速览 */
    var grid = $("#home-counters");
    if(grid){
      grid.innerHTML = "";
      (counters||[]).forEach(function(c){
        var a = document.createElement("a");
        a.className = "card";
        a.href = "counter" + c.id.replace("c","") + ".html";
        a.innerHTML =
          '<h3>' + esc(c.name) + '</h3>' +
          '<div class="card-dept">' + esc(c.dept) + '</div>' +
          '<p>' + esc(c.intro) + '</p>' +
          '<span class="more">查看业务 →</span>';
        grid.appendChild(a);
      });
    }

    /* 宣传视频 */
    var vw = $("#promo-video");
    if(vw){
      if(s.videoUrl){
        var video = document.createElement("video");
        video.controls = true; video.preload = "metadata";
        if(s.videoPoster){ video.poster = s.videoPoster; }
        var src = document.createElement("source");
        src.src = s.videoUrl; src.type = "video/mp4";
        video.appendChild(src);
        vw.appendChild(video);
        vw.classList.remove("hidden");
      }
    }

    /* 轮播图（首页上半部分，每张可带跳转链接） */
    var carousel = $("#hero-carousel");
    var fb = $("#hero-fallback");
    var imgs = s.banners || [];
    if(imgs.length === 0){
      if(carousel){ carousel.classList.add("hidden"); }
      if(fb){ fb.classList.remove("hidden"); }
    }else{
      if(fb){ fb.classList.add("hidden"); }
      if(carousel){
        carousel.classList.remove("hidden");
        carousel.innerHTML = "";
        imgs.forEach(function(b, i){
          var div = document.createElement("div");
          div.className = "slide" + (i===0 ? " active" : "");
          var inner = '<img src="' + esc(b.img) + '" alt="' + esc(b.title||"") + '">' +
                      (b.title ? '<div class="slide-cap">' + esc(b.title) + '</div>' : "");
          if(b.link){
            div.innerHTML = '<a href="' + esc(b.link) + '" target="_blank" rel="noopener">' + inner + '</a>';
          }else{
            div.innerHTML = inner;
          }
          carousel.appendChild(div);
        });
        var idx = 0, slides = $$(".slide", carousel);
        setInterval(function(){
          if(slides.length < 2){ return; }
          slides[idx].classList.remove("active");
          idx = (idx+1) % slides.length;
          slides[idx].classList.add("active");
        }, 4500);
      }
    }
  }

  /* =========================================================
     页面：柜台列表
     ========================================================= */
  function renderCounterList(counters){
    var grid = $("#counter-list");
    if(!grid){ return; }
    grid.innerHTML = "";
    (counters||[]).forEach(function(c){
      var a = document.createElement("a");
      a.className = "card";
      a.href = "counter" + c.id.replace("c","") + ".html";
      a.innerHTML =
        '<h3>' + esc(c.name) + '</h3>' +
        '<div class="card-dept">' + esc(c.dept) + '</div>' +
        '<p>' + esc(c.intro) + '</p>' +
        '<span class="more">' + esc(c.services.length) + ' 项业务，查看详情 →</span>';
      grid.appendChild(a);
    });
  }

  /* =========================================================
     页面：柜台详情
     ========================================================= */
  function renderCounterDetail(counters, cid){
    var c = (counters||[]).filter(function(x){ return x.id === cid; })[0];
    if(!c){ return; }
    var head = $("#counter-head");
    if(head){
      head.textContent = c.name + " · 业务详情";
    }
    var dept = $("#counter-dept");
    if(dept){ dept.textContent = c.dept; }
    var intro = $("#counter-intro-text");
    if(intro){ intro.textContent = c.intro; }

    var nav = $("#counter-nav");
    if(nav){
      nav.innerHTML = "";
      (counters||[]).forEach(function(x){
        var a = document.createElement("a");
        a.href = "counter" + x.id.replace("c","") + ".html";
        a.textContent = x.name;
        if(x.id === cid){ a.classList.add("active"); }
        nav.appendChild(a);
      });
    }

    var list = $("#service-list");
    if(list){
      list.innerHTML = "";
      (c.services||[]).forEach(function(svc, i){
        var div = document.createElement("div");
        div.className = "service-item";
        var tipsHtml = "";
        if(svc.tips && svc.tips.length){
          tipsHtml = '<div class="tips-title">注意事项</div><ul class="tips">' +
            svc.tips.map(function(t){ return '<li>' + esc(t) + '</li>'; }).join("") + '</ul>';
        }
        div.innerHTML =
          '<h3><span class="svc-no">' + (i+1) + '</span>' + esc(svc.name) + '</h3>' +
          '<p class="svc-desc">' + esc(svc.desc) + '</p>' + tipsHtml;
        list.appendChild(div);
      });
    }
  }

  /* =========================================================
     页面：值班安排
     ========================================================= */
  function dateToWeekCN(dateStr){
    var p = String(dateStr).split("-");
    var d = new Date(+p[0], (+p[1]||1)-1, +p[2]||1);
    return dayLabelCN(["sun","mon","tue","wed","thu","fri","sat"][d.getDay()]);
  }
  function weekRange(){
    var n = new Date();
    var day = n.getDay() || 7;
    var mon = new Date(n); mon.setDate(n.getDate() - day + 1);
    var sun = new Date(mon); sun.setDate(mon.getDate() + 6);
    function fmt(d){ return d.getFullYear() + "-" + String(d.getMonth()+1).padStart(2,"0") + "-" + String(d.getDate()).padStart(2,"0"); }
    return [fmt(mon), fmt(sun)];
  }

  function renderShiftTable(sched){
    var box = $("#shift-table");
    if(!box){ return; }
    var shifts = sched.shifts || [];
    var days = ["mon","tue","wed","thu","fri"];
    var tk = todayKey();
    var range = weekRange();
    var ex = (sched.exceptions||[]).filter(function(e){
      return e.date >= range[0] && e.date <= range[1];
    });

    var table = document.createElement("table");
    table.className = "shift-grid";
    var thead = document.createElement("thead");
    var hr = document.createElement("tr");
    var th0 = document.createElement("th");
    th0.textContent = "班次时间";
    hr.appendChild(th0);
    days.forEach(function(k){
      var th = document.createElement("th");
      th.textContent = dayLabelCN(k);
      if(k === tk){ th.classList.add("is-today"); }
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    table.appendChild(thead);

    var tbody = document.createElement("tbody");
    shifts.forEach(function(shift){
      var tr = document.createElement("tr");
      var td0 = document.createElement("td");
      td0.className = "shift-time";
      td0.textContent = shift;
      tr.appendChild(td0);
      days.forEach(function(k){
        var td = document.createElement("td");
        if(k === tk){ td.classList.add("is-today"); }
        var recs = ex.filter(function(e){
          if(dateToWeekCN(e.date) !== dayLabelCN(k)){ return false; }
          if(e.type === "暂停"){ return true; }
          if(e.shift && e.shift !== "全天"){ return e.shift === shift; }
          return true;
        });
        if(recs.length){
          var paused = recs.some(function(r){ return r.type === "暂停"; });
          td.classList.add("cell-bad");
          if(paused){
            td.innerHTML = '<span class="cell-tag bad">暂停</span>';
          }else{
            var who = [];
            recs.forEach(function(r){
              (r.counters||[]).forEach(function(c){
                var nm = (sched.counterNames||{})[c] || c;
                if(who.indexOf(nm) < 0){ who.push(nm); }
              });
            });
            td.innerHTML = '<span class="cell-tag bad">空班</span>' +
              (who.length ? '<span class="cell-note">' + esc(who.join("、")) + '</span>' : "");
          }
        }else{
          td.classList.add("cell-ok");
          td.innerHTML = '<span class="cell-tag ok">正常值班</span>';
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    box.innerHTML = "";
    box.appendChild(table);
  }

  function renderExceptions(sched){
    var tl = $("#exception-list");
    if(!tl){ return; }
    var ex = (sched.exceptions||[]).slice().sort(function(a,b){ return a.date < b.date ? 1 : -1; });
    if(ex.length === 0){
      tl.innerHTML = '<div class="empty">近期暂无临时变更。如有空班或暂停安排，管理员在 <code>data/schedule.json</code> 的 exceptions 中新增一条即可。</div>';
      return;
    }
    tl.innerHTML = '<div class="timeline"></div>';
    var tlBox = $(".timeline", tl);
    ex.forEach(function(e){
      var div = document.createElement("div");
      div.className = "t-item";
      var who = "";
      if(e.counters && e.counters.length){
        who = "（" + e.counters.map(function(c){ return sched.counterNames[c] || c; }).join("、") + "）";
      }
      var shiftTxt = e.shift && e.shift !== "全天" ? " · " + e.shift : "";
      div.innerHTML =
        '<div class="t-date">' + esc(e.date) + '（' + esc(dateToWeekCN(e.date)) + '）' + '</div>' +
        '<div class="t-title">' + esc(e.type) + who + shiftTxt + '</div>' +
        (e.note ? '<div class="t-note">' + esc(e.note) + '</div>' : "");
      tlBox.appendChild(div);
    });
  }

  function renderSchedule(sched){
    renderStatusBanner(sched);
    renderShiftTable(sched);
    renderExceptions(sched);
  }

  /* =========================================================
     页面：通知公告
     ========================================================= */
  function renderNotices(notices){
    var list = $("#notice-list");
    if(!list){ return; }
    var all = (notices||[]).slice().sort(function(a,b){ return a.date < b.date ? 1 : -1; });
    if(all.length === 0){
      list.innerHTML = '<div class="empty">暂无通知公告。管理员在 <code>data/notices.json</code> 中新增条目即可发布。</div>';
      return;
    }
    list.innerHTML = "";
    all.forEach(function(n){
      var div = document.createElement("div");
      div.className = "notice-item";
      var tagHtml = n.tag ? '<span class="tag' + (n.tag==="重要" ? " hot" : "") + '">' + esc(n.tag) + '</span>' : "";
      var linkHtml = "";
      if(n.link){
        linkHtml = '<a class="n-link" href="' + esc(n.link) + '" target="_blank" rel="noopener">' + esc(n.linkText||"查看原文") + ' →</a>';
      }
      div.innerHTML =
        '<div class="n-head"><span class="n-title">' + esc(n.title) + '</span>' + tagHtml +
        '<span class="n-date">' + esc(n.date) + '</span></div>' +
        (n.body ? '<p class="n-body">' + esc(n.body) + '</p>' : "") + linkHtml;
      list.appendChild(div);
    });
  }

  /* =========================================================
     页面：关于我们
     ========================================================= */
  function renderAbout(s){
    var el = $("#about-facts");
    if(el){
      el.innerHTML =
        '<li><span class="k">成立时间</span>' + esc(s.founded || "2023年6月") + '</li>' +
        '<li><span class="k">办公地点</span>' + esc(s.address) + '</li>' +
        '<li><span class="k">工作时间</span>' + esc(s.hours) + '</li>' +
        '<li><span class="k">联系邮箱</span><a href="mailto:' + esc(s.email) + '">' + esc(s.email) + '</a></li>' +
        (s.officialAccount ? '<li><span class="k">微信公众号</span>' + esc(s.officialAccount) + '</li>' : "");
    }
    var vw = $("#promo-video");
    if(vw && s.videoUrl){
      var video = document.createElement("video");
      video.controls = true; video.preload = "metadata";
      if(s.videoPoster){ video.poster = s.videoPoster; }
      var src = document.createElement("source");
      src.src = s.videoUrl; src.type = "video/mp4";
      video.appendChild(src);
      vw.appendChild(video);
      vw.classList.remove("hidden");
    }
  }

  /* ---------- 启动 ---------- */
  initNav();

  var needSettings = NAV !== "";
  var settingsP = loadJSON("data/settings.json").catch(function(e){ console.warn(e); return {}; });

  settingsP.then(function(s){
    renderFooter(s);
    if(PAGE === "about"){ renderAbout(s); }
  });

  var job = settingsP;

  if(PAGE === "home"){
    job = Promise.all([
      settingsP,
      loadJSON("data/schedule.json").catch(function(){ return {}; }),
      loadJSON("data/notices.json").catch(function(){ return []; }),
      loadJSON("data/counters.json").catch(function(){ return {counters:[]}; })
    ]).then(function(d){
      renderHome(d[0], d[1], d[2], d[3].counters||[]);
    });
  }else if(PAGE === "counters"){
    job = loadJSON("data/counters.json").catch(function(){ return {counters:[]}; })
      .then(function(d){ renderCounterList(d.counters||[]); });
  }else if(PAGE === "counter-detail"){
    job = loadJSON("data/counters.json").catch(function(){ return {counters:[]}; })
      .then(function(d){ renderCounterDetail(d.counters||[], document.body.getAttribute("data-counter")||"c1"); });
  }else if(PAGE === "schedule"){
    job = loadJSON("data/schedule.json").catch(function(){ return {}; })
      .then(function(d){ renderSchedule(d); });
  }else if(PAGE === "notices"){
    job = loadJSON("data/notices.json").catch(function(){ return []; })
      .then(function(d){ renderNotices(d); });
  }

  job.catch(function(e){ console.error("站点数据加载失败：", e); });
})();
