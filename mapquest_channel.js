/*
{
    "targets": ["17325134403", "15164264399"],
    "location": "40.709847, -73.986318"
}
*/
export default (request) => {
    function addressFromJSON(data){
        var result = data.results[0];
        var location = result.locations[0];
        return location.street + " " + location.adminArea5 + ", " + location.adminArea3;
    }
    
    let xhr = require('xhr');
    let query = require('codec/query_string');
    const pubnub = require("pubnub");

    let clientToken = "1CgjzZA0gGXgFKBQJm1DddsSg9oMK78C";
    let apiUrl = 'http://www.mapquestapi.com/geocoding/v1/reverse';
    let searchParam = request.message.location;
    console.log(searchParam);

    // return if the block does not have anything to analyze
    if (!query) {
        return request.ok();
    }

    let queryParams = {
        key: clientToken,
        location: searchParam,
    };

    let url = apiUrl + '?' + query.stringify(queryParams);
    console.log(url);

    return xhr.fetch(url)
        .then((response) => {
            return response.json()
                .then((parsedResponse) => {
                    var address = addressFromJSON(parsedResponse);
                    request.message.text = "Hello from " + address;
                    
                    pubnub.publish({
                        "channel": "neximo_channel",
                        "message": request.message
                    });
                    
                    return request;
                })
                .catch((err) => {
                    console.log('error happened on JSON parse', err);
                    return request;
                });
        })
        .catch((err) => {
            console.log('error happened for XHR.fetch', err);
            return request;
        });

};

