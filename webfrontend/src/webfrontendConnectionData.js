// Retrieve webfrontend connection data
//  If service call returns an error provide static development values
import axios from 'axios'
// import callbackHelper from 'callbackHelper'

function getData (callback) {
  var config = {
    method: 'GET',
    url: 'webfrontendConnectionData'
  }
  axios(config).then(
    (response) => {
      callback.ok(response)
    },
    (response) => {
      callback.ok({ data: {
        version: 'Development', // Version show as 0 fom this file
        apiurl: 'http://localhost:80/dockjobapi',
        apiaccesssecurity: [] // all supported auth types. Can be empty, or strings: basic-auth, jwt
        // Empty list means no auth type
        //  { type: basic-auth } - webfrontend will prompt user for username and password
        //  ...
      }})
    }
  )
}

export default getData
