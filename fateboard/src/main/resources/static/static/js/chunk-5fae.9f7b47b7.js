(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-5fae"],{C9MU:function(n,t,e){var i=e("RMZv");"string"==typeof i&&(i=[[n.i,i,""]]),i.locals&&(n.exports=i.locals);(0,e("SZ7m").default)("9e62a6e4",i,!0,{})},RMZv:function(n,t,e){(n.exports=e("I1BE")(!1)).push([n.i,".running-container {\n  height: 100%;\n  padding: 50px 0;\n}\n.running-container .job-list > li {\n    width: 336px;\n    height: 240px;\n    margin: 12px;\n    background: #fff;\n    border-radius: 5px;\n}\n.running-container .job-list > li .top {\n      padding: 10px;\n}\n.running-container .job-list > li .top .enter {\n        width: 72px;\n        text-align: center;\n        height: 22px;\n        line-height: 22px;\n        border-radius: 22px;\n}\n.running-container .job-list > li .top .enter:hover {\n          background: #e8e8ef;\n}\n.running-container .job-list > li .status {\n      height: 188.16px;\n}\n.running-container .job-list > li .status .text {\n        left: 50%;\n        top: 50%;\n        width: 100px;\n        height: 100px;\n        margin-left: -50px;\n        margin-top: -50px;\n        text-align: center;\n        line-height: 100px;\n}\n.running-container .job-list > li .status .mask {\n        z-index: 999;\n        display: none;\n        background: rgba(255, 255, 255, 0.5);\n}\n.running-container .job-list > li .status .el-button {\n        display: none;\n}\n.running-container .job-list > li .status:hover .mask {\n        display: -webkit-box;\n        display: -ms-flexbox;\n        display: flex;\n}\n.running-container .job-list > li .status:hover .el-button {\n        display: block;\n}\n",""])},"b/+g":function(n,t,e){"use strict";e.r(t);var i=e("dv4G"),o={components:{},directives:{},data:function(){return{loading:!0,jobList:[]}},mounted:function(){this.getJobList()},methods:{getJobList:function(){var n=this;this.jobList=[],this.loading=!0,Object(i.b)().then(function(t){n.loading=!1,t.data.forEach(function(t){var e=t.fJobId,i=t.fStatus,o=t.fProgress||0,r="running"===i?o+"%":i;n.jobList.push({jobId:e,fStatus:i,status:r,statusProgress:"running"===i?o:0})})})},enter:function(n){this.$router.push({path:"/dashboard",query:{jobId:n}})},handleKillJob:function(n){var t=this;this.$confirm("You can't undo this action","Are you sure you want to kill this job?",{confirmButtonText:"Sure",cancelButtonText:"Cancel",type:"warning"}).then(function(){t.submitKillJob(n)}).catch(function(){console.log("cancel kill")})},submitKillJob:function(n){var t=this;Object(i.g)(n).then(function(e){console.log("kill job:"+n),t.getJobList()})}}},r=(e("jfYB"),e("KHd+")),s=Object(r.a)(o,function(){var n=this,t=n.$createElement,e=n._self._c||t;return e("div",{directives:[{name:"loading",rawName:"v-loading",value:n.loading,expression:"loading"}],staticClass:"running-container flex flex-center flex-col app-container"},[e("ul",{staticClass:"job-list flex flex-center flex-wrap"},n._l(n.jobList,function(t){return e("li",{key:t.jobId,staticClass:"shadow"},[e("div",{staticClass:"top flex flex-center space-between"},[e("span",{staticClass:"job-id text-primary"},[n._v(n._s(t.jobId))]),n._v(" "),e("span",{staticClass:"enter text-primary pointer",on:{click:function(e){n.enter(t.jobId)}}},[n._v("Enter "),e("i",{staticClass:"el-icon-right"})])]),n._v(" "),e("div",{staticClass:"status pos-r flex flex-center justify-center"},[e("span",{staticClass:"text pos-a text-primary",style:{"font-size":"waiting"===t.status||"faied"===t.status?"14px":"36px"}},[n._v(n._s(t.status))]),n._v(" "),e("div",{staticClass:"mask pos-a wh-100 flex flex-center justify-center",style:{display:"waiting"===t.status?"flex":""}},[e("el-button",{attrs:{round:""},on:{click:function(e){n.handleKillJob(t.jobId)}}},[n._v("kill")])],1),n._v(" "),e("el-progress",{attrs:{percentage:t.statusProgress,"show-text":!1,width:120,color:"#494ece",type:"circle"}})],1)])}))])},[],!1,null,null,null);s.options.__file="index.vue";t.default=s.exports},dv4G:function(n,t,e){"use strict";e.d(t,"a",function(){return o}),e.d(t,"f",function(){return r}),e.d(t,"b",function(){return s}),e.d(t,"g",function(){return a}),e.d(t,"e",function(){return u}),e.d(t,"d",function(){return l}),e.d(t,"c",function(){return c}),e.d(t,"h",function(){return d});var i=e("t3Un");function o(n){var t=n.total,e=n.pno,o=n.psize,r=void 0===o?10:o;return Object(i.a)({url:"/job/query/all/"+t+"/"+e+"/"+r,method:"get",params:{}})}function r(){return Object(i.a)({url:"/job/query/totalrecord",method:"get",params:{}})}function s(n){return Object(i.a)({url:"/job/query/status",method:"get",params:n})}function a(n){return Object(i.a)({url:"/job/v1/pipeline/job/stop",method:"post",data:{job_id:n}})}function u(n){return Object(i.a)({url:"/job/query/"+n,method:"get"})}function l(n){return Object(i.a)({url:"/v1/pipeline/dag/dependencies",method:"post",data:{job_id:n}})}function c(n){return Object(i.a)({url:"/v1/tracking/component/parameters",method:"post",data:n})}function d(n){var t=n.componentId,e=n.jobId,o=n.begin,r=n.end,s=n.type,a=void 0===s?"default":s;return Object(i.a)({url:"/queryLogWithSize/"+t+"/"+e+"/"+a+"/"+o+"/"+r+"  ",method:"get"})}},jfYB:function(n,t,e){"use strict";var i=e("C9MU");e.n(i).a}}]);