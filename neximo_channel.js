/*

{
    "targets": ["17325134403", "15164264399"],
    "text": "Test msg lol"
}

 */

export default (request) => { 
    let xhr = require('xhr');
    let query = require('codec/query_string');
    
    if (!query) {
        return request.ok();
    }
    
    let targets = request.message.targets;
    let text = request.message.text;
    request.message.responses = [];
    for (var i = 0; i < targets.length; i++){
        var target = targets[i];
        let params = {
            api_key: "95678560",
            api_secret: "25715ea8b0f57094",
            to: target.toString(),
            from: "12035298957",
            text: text
        };
        let url = "https://rest.nexmo.com/sms/json" + "?" + query.stringify(params);
        
        xhr.fetch(url)
            .then((response) => {
                response.json()
                    .then((parsedResponse) => {
                        request.message.responses.push(parsedResponse);
                    })
                    .catch((err) => {
                        console.log('error happened on JSON parse', err);
                        request.message.responses.push(err);
                    });
            })
            .catch((err) => {
                console.log('error happened for XHR.fetch', err);
                request.message.responses.push(err);
            });
    }

    return request.ok(); // Return a promise when you're done 
}
