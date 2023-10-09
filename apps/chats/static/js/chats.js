const defaultChannel = "coolrom"

const protocol = window.location.protocol == "http:" ? "ws" : "wss";
const ws = new WebSocket(`${protocol}://${window.location.host}/ws/${defaultChannel}/`);

setupElements();
setupWebsocket();

function setupWebsocket() {
  ws.onopen = function (e) {
    console.log("The connection was setup successfully !");
  };

  ws.onclose = function (e) {
    console.log("Something unexpected happened !", e);
  };

  ws.onmessage = function (e) {
    const data = JSON.parse(e.data);
    createMessageEle(data.username + ": " + data.message);
  };
}

function setupElements() {
  document.querySelector("#message_input").focus();
  document.querySelector("#message_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
      document.querySelector("#send_button").click();
    }
  };
  document.querySelector("#send_button").onclick = function (e) {
    var message = document.querySelector("#message_input").value;
    var username = document.querySelector("#logged-in-user").innerHTML;
    sendMesage({ message, username });
  };
}

function sendMesage({ message, username }) {
  ws.send(JSON.stringify({ message, username }));
}

function createMessageEle(message) {
  var container = document.createElement("div");
  container.innerHTML = message;
  document.querySelector("#message_input").value = "";
  document.querySelector("#chat_box_container").appendChild(container);
}


