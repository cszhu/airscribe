/**
 * Copyright 2015 IBM Corp. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
/* global $ */
'use strict';

var display = require('./views/displaymetadata');
var initSocket = require('./socket').initSocket;

exports.handleFileUpload = function(type, token, model, file, contentType, callback, onend) {

    // Set currentlyDisplaying to prevent other sockets from opening
    localStorage.setItem('currentlyDisplaying', type);

    // $('#progressIndicator').css('visibility', 'visible');

    $.subscribe('progress', function(evt, data) {
      console.log('progress: ', data);
    });

    console.log('contentType', contentType);

    var baseString = '';
    var baseJSON = '';

    $.subscribe('showjson', function() {
      var $resultsJSON = $('#resultsJSON');
      $resultsJSON.empty();
      $resultsJSON.append(baseJSON);
    });

    var options = {};
    options.token = token;
    options.message = {
      'action': 'start',
      'content-type': contentType,
      'interim_results': true,
      'continuous': true,
      'word_confidence': true,
      'timestamps': true,
      'max_alternatives': 3,
      'inactivity_timeout': 600
    };
    options.model = model;

    function onOpen() {
      console.log('Socket opened');
    }

    function onListening(socket) {
      console.log('Socket listening');
      callback(socket);
    }

    function onMessage(msg) {
      if (msg.results) {
        // Convert to closure approach
        baseString = display.showResult(msg, baseString, model);
        baseJSON = display.showJSON(msg, baseJSON);
      }
    }

    function onError(evt) {
      localStorage.setItem('currentlyDisplaying', 'false');
      onend(evt);
      console.log('Socket err: ', evt.code);
    }

    function onClose(evt) {
      localStorage.setItem('currentlyDisplaying', 'false');
      onend(evt);
      console.log('Socket closing: ', evt);

      var finalText = document.getElementById('resultsText').value;
      console.log(finalText);

      var url = 'http://ec2-52-33-131-240.us-west-2.compute.amazonaws.com:5000/give_text';

      $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify({text: finalText}),
            contentType: 'application/json; charset=utf-8',
            dataType: "json",
            success: function(data) {
              console.log(data);
            },
            error: function(data) {
              console.log(data.responseText);
              var raw = data.responseText;
              var sentences = raw.split('\n');
              document.getElementById('interview-results').innerHTML="";

              var node, boldNode, boldText, div, textNode, text;
              node = document.createElement('h2');
              boldNode = document.createElement('b');
              boldText = document.createTextNode(sentences[0]);
              boldNode.appendChild(boldText);
              node.appendChild(boldNode);
              console.log(node);
              document.getElementById('interview-results').appendChild(node);

              var i = 1;
              while(sentences[i].search("Airscribe") == -1) {
                var current = sentences[i];
                if (current.search("\\?") > 0 ) {
                  console.log("a q question");
                  console.log(current);
                  i++;
                  var next = sentences[i];
                  console.log(next);
                  addBoldAndAnswer(current, next);
                  i++;
                } else if ((current.search(":") > 0) && (current.search("A") == -1)) {
                  var substrings = current.split(":");
                  addBoldAndAnswer(substrings[0], substrings[1]);
                  i++;
                } else {
                  addBoldAndAnswer(current, "");
                  i++;
                }
              }

              function addBoldAndAnswer(a, b) {
                var node, boldNode, boldText, div, textNode, text;
                node = document.createElement('p');
                boldNode = document.createElement('b');
                textNode = document.createElement('p');
                boldText = document.createTextNode(a);
                text = document.createTextNode(b);
                boldNode.appendChild(boldText);
                textNode.appendChild(text);
                node.appendChild(boldNode);
                node.appendChild(textNode);
                console.log(node);
                document.getElementById('interview-results').appendChild(node);
              }

            }
          });
    }

    initSocket(options, onOpen, onListening, onMessage, onError, onClose);
};
