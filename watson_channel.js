/*
{
    text: "Swiggity swooty, comin for that booty"
}
 */ 

// require console module
const console = require('console');

// require xhr
const xhr = require('xhr');

// require state for storing watson token
const store = require('kvstore');

const query = require('codec/query_string');

const auth = require('codec/auth');

export default (request) => {

    // watson api token
    const username = '8db5f588-5ce2-407c-9f18-7058316be508';

    const password = 'brLJy4WtmWtz';

    // translation api url
    const apiUrl =
        'https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize';

    // token url
    const tokenUrl = 'https://stream.watsonplatform.net/authorization/api/v1/token?url=https://stream.watsonplatform.net/text-to-speech/api';

    //  Since this is a before publish event hanlder, we can modify the
    // message and subscribers will receive modified version.

    return store.get('watson_token').then((watsonToken) => {

        watsonToken = watsonToken || { token: null, timestamp: null };

        let response = request.ok();

        if (watsonToken.token === null ||
                (Date.now() - watsonToken.timestamp) > 3000000) {

            const httpOptions = {
                as: 'json',
                headers: {
                    Authorization: auth.basic(username, password)
                }
            };


            response = xhr.fetch(tokenUrl, httpOptions).then(r => {

                watsonToken.token = decodeURIComponent(r.body);
                watsonToken.timestamp = Date.now();
                store.set('watson_token', watsonToken);
                if (watsonToken.token) {
                    const queryParams = {
                        accept: 'audio/wav',
                        voice: 'en-US_AllisonVoice',
                        text: request.message.text,
                        'watson-token': watsonToken.token
                    };

                    request.message.speech =
                    apiUrl + '?' + query.stringify(queryParams);
                }
                console.log(request.message.speech);
                return request.ok();

            },
            e => console.error(e.body))
            .catch((e) => console.error(e));
        } else {

            const queryParams = {
                accept: 'audio/wav',
                voice: 'en-US_AllisonVoice',
                text: request.message.text,
                'watson-token': watsonToken.token
            };

            request.message.speech = apiUrl + '?' + query.stringify(queryParams);

            console.log(request.message.speech);
        }

        return response;


    });

};

