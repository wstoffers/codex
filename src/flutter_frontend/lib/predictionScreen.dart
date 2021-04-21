import 'dart:developer';

import 'package:flutter/material.dart';

import 'carouselSlider.dart';
import 'carouselOptions.dart';

class PredictionScreen extends StatefulWidget {
  static const routeName = '/prediction';
  final String title;
  final String credit;
  final String ingredients;
  final List<String> predictions;

  const PredictionScreen({
    Key key,
    this.title,
    this.credit,
    this.ingredients,
    this.predictions,
  }) : super(key: key);

  @override
  State<StatefulWidget> createState() {
    return _CarouselWithIndicatorState(
      title,
      credit,
      ingredients,
      predictions,
    );
  }
}

class _CarouselWithIndicatorState extends State<PredictionScreen> {
  int _current = 0;
  String title;
  String credit;
  String ingredients;
  List<String> predictions;
  List<Widget> imageSliders;
  List<String> imageList = [
    'Old-Fashioned',
    'Martini',
    'Daiquiri',
    'Sidecar',
    'Whiskey Highball',
    'Flip',
  ];

  _CarouselWithIndicatorState(
    this.title,
    this.credit,
    this.ingredients,
    this.predictions,
  );

  @override
  Widget build(BuildContext context) {
    imageSliders = predictions
        .map((item) => Container(
              child: Container(
                margin: EdgeInsets.all(5.0),
                child: ClipRRect(
                  borderRadius: BorderRadius.all(Radius.circular(5.0)),
                  child: Stack(
                    children: <Widget>[
                      Container(
                        constraints: BoxConstraints(
                            minWidth: MediaQuery.of(context).size.width * .5,
                            maxWidth: MediaQuery.of(context).size.width * .9),
                        color: Colors.black,
                        child: Center(
                          child: Text(item, textAlign: TextAlign.center),
                        ),
                      ),
                      Positioned(
                        bottom: 0.0,
                        left: 0.0,
                        right: 0.0,
                        child: Container(
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Color.fromARGB(200, 0, 0, 0),
                                Color.fromARGB(0, 0, 0, 0)
                              ],
                              begin: Alignment.bottomCenter,
                              end: Alignment.topCenter,
                            ),
                          ),
                          padding: EdgeInsets.symmetric(
                              vertical: 10.0, horizontal: 20.0),
                          child: Text(
                            item,
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 20.0,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ))
        .toList();
    return Scaffold(
      body: Column(
        children: [
          CarouselSlider(
            items: imageSliders,
            options: CarouselOptions(
                autoPlay: false,
                enlargeCenterPage: true,
                aspectRatio: 2.0,
                onPageChanged: (index, reason) {
                  setState(() {
                    _current = index;
                  });
                }),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: imageList.map((url) {
              int index = imageList.indexOf(url);
              return Container(
                width: 8.0,
                height: 8.0,
                margin: EdgeInsets.symmetric(vertical: 10.0, horizontal: 2.0),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: _current == index
                      ? Color.fromRGBO(0, 0, 0, 0.9)
                      : Color.fromRGBO(0, 0, 0, 0.4),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
