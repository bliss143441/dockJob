// This class contains functions to help callbacks

function callbackWithError (callback, msg, obj) {
  var retobj = {
    message: msg,
    orig: obj
  }
  console.log(retobj)
  callback.error(retobj)
}
function callbackWithSimpleError (callback, msg) {
  callbackWithError(callback, msg, undefined)
}
function callbackWithNotImplemented (callback) {
  callbackWithError(callback, 'Not Implemented', undefined)
}

// Used as the error function of an axios call
function webserviceError (callback, response) {
  var rjmmsg = 'Error'

  if (typeof (response.response) === 'undefined') {
    if (typeof (response.message) === 'undefined') {
      rjmmsg = 'Bad Response UNKNOWN'
    }
    else {
      rjmmsg = 'Bad Response ' + response.message
    }
  }
  else if (typeof (response.response.data) !== 'undefined') {
    if (typeof (response.response.data.errorMessages) !== 'undefined') {
      rjmmsg = 'Bad Response(' + response.response.data.errorMessages.length + ') ' + response.response.data.errorMessages
    }
    else {
      rjmmsg = 'Data Bad Response ' + response.response.status
    }
  }
  else {
    rjmmsg = 'Nested Bad Response ' + response.response.status
  }
  callbackWithError(callback, rjmmsg, response)
}

export default {
  callbackWithError: callbackWithError,
  callbackWithSimpleError: callbackWithSimpleError,
  callbackWithNotImplemented: callbackWithNotImplemented,
  webserviceError: webserviceError
}
