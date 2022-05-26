import Vue from "vue"
import sanitizeHTML from "sanitize-html"

sanitizeHTML.defaults.allowedTags.push("table");
sanitizeHTML.defaults.allowedTags.push("tbody");
sanitizeHTML.defaults.allowedTags.push("tr");
sanitizeHTML.defaults.allowedTags.push("td");
sanitizeHTML.defaults.allowedTags.push("lite-youtube");
sanitizeHTML.defaults.allowedAttributes["table"] = ["style", "border"]
sanitizeHTML.defaults.allowedAttributes["tbody"] = ["style"]
sanitizeHTML.defaults.allowedAttributes["tr"] = ["style"]
sanitizeHTML.defaults.allowedAttributes["td"] = ["style"]
sanitizeHTML.defaults.allowedAttributes["p"] = ["style"]
sanitizeHTML.defaults.allowedAttributes["span"] = ["style"]
sanitizeHTML.defaults.allowedAttributes["lite-youtube"] = ["videoid", "params", "class"]

Vue.prototype.$sanitize = sanitizeHTML
