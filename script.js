// Create a client instance
let client;
// set callback handlers

function MQTTconnect() {
    client = new Paho.MQTT.Client('130.237.59.45', 9001, "MonjolaJavascript");
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;
    client.connect({ onSuccess: onConnect });
}
// connect the client



// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe("test/topic");
    message = new Paho.MQTT.Message("Javascript connected");
    message.destinationName = "test/topic";
    client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}

// called when a message arrives
function onMessageArrived(message) {
    console.log("onMessageArrived:" + message.payloadString);
    
}
function sendcordinate(msg) {
    let distance = ''
    if (document.getElementById('10mm').checked) {
        distance = '10';
    } else if (document.getElementById('100mm').checked) {
        distance = '100';
    } else {
        distance = '1';
    }
    console.log(distance)
    msg = msg + distance;
    message = new Paho.MQTT.Message(msg);
    message.destinationName = "test/topic";
    client.send(message);
}
function turnonoff(status) {
    const onoffmsg = new Paho.MQTT.Message(status);
    onoffmsg.destinationName = "test/topic";
    client.send(onoffmsg);
}