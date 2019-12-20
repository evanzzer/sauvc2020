// Auto-generated. Do not edit!

// (in-package sauvc.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class lokasi {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.xloc = null;
    }
    else {
      if (initObj.hasOwnProperty('xloc')) {
        this.xloc = initObj.xloc
      }
      else {
        this.xloc = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type lokasi
    // Serialize message field [xloc]
    bufferOffset = _serializer.uint8(obj.xloc, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type lokasi
    let len;
    let data = new lokasi(null);
    // Deserialize message field [xloc]
    data.xloc = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a message object
    return 'sauvc/lokasi';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '82f34519e751e2caec3eadc7bc50234e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 xloc
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new lokasi(null);
    if (msg.xloc !== undefined) {
      resolved.xloc = msg.xloc;
    }
    else {
      resolved.xloc = 0
    }

    return resolved;
    }
};

module.exports = lokasi;
