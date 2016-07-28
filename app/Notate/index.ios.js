'use strict';

import React, { Component } from 'react';
import {
  AppRegistry,
  TabBarIOS,
  StyleSheet,
  Dimensions,
  ListView,
  Text,
  View,
  TouchableHighlight
} from 'react-native'

import Camera from 'react-native-camera';

var Game = require('./game.ios');
var Notes = require('./notes.ios');
var Load = require('./load.ios');

class Notate extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedTab: 'game'
    };
  }

  render() {
    return (
      <TabBarIOS selectedTab={this.state.selectedTab}>

      <TabBarIOS.Item
      selected={this.state.selectedTab === 'game'}
      // icon={{uri:'gameplay'}}
      title='Game'
      onPress={() => {
        this.setState({
          selectedTab: 'game'
        });
      }}>
      <Game />
      </TabBarIOS.Item>

      <TabBarIOS.Item
      selected={this.state.selectedTab === 'load'}
      // icon={{uri:'notations'}}
      title="Upload"
      onPress={() => {
        this.setState({
          selectedTab: 'load'
        });
      }}>
      <Load />
      </TabBarIOS.Item>

      <TabBarIOS.Item
      selected={this.state.selectedTab === 'notes'}
      // icon={{uri:'notations'}}
      title="Notations"
      onPress={() => {
        this.setState({
          selectedTab: 'notes'
        });
      }}>
      <Notes />
      </TabBarIOS.Item>

      </TabBarIOS>
    )
  }
}

AppRegistry.registerComponent('Notate', () => Notate);
