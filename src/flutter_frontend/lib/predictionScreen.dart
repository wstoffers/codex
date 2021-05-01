import 'package:flutter/material.dart';

import 'carouselSlider.dart';
import 'carouselOptions.dart';

class PredictionScreen extends StatefulWidget {
  static const routeName = '/prediction';
  final String title;
  final String credit;
  final String ingredients;
  final List predictions;

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
  List predictions;
  List<Widget> imageSliders;

  /*
  Map<String, Image> images = {
    'Old-Fashioned': Image.network(
      'https://storage.googleapis.com/wstoffers-galvanize-codex-public/oldFashioned.JPG',
      width: 1000,
      fit: BoxFit.fitWidth,
    ),
    'Martini': Image.network(
      'https://storage.googleapis.com/wstoffers-galvanize-codex-public/martini.JPG',
      width: 1000,
      fit: BoxFit.fitWidth,
    ),
    'Daiquiri': Image.network(
      'https://storage.googleapis.com/wstoffers-galvanize-codex-public/daiquiri.JPG',
      width: 1000,
      fit: BoxFit.fitWidth,
    ),
    'Sidecar': Image.network(
      'https://storage.googleapis.com/wstoffers-galvanize-codex-public/sidecar.JPG',
      width: 1000,
      fit: BoxFit.fitWidth,
    ),
    'Whisky Highball': Image.network(
      'https://storage.googleapis.com/wstoffers-galvanize-codex-public/highball.JPG',
      width: 1000,
      fit: BoxFit.fitWidth,
    ),
    'Flip': Image.network(
      'https://storage.googleapis.com/wstoffers-galvanize-codex-public/flip.JPG',
      width: 1000,
      fit: BoxFit.fitWidth,
    ),
  };*/
  Map<String, String> images = {
    'Old-Fashioned': 'assets/images/oldFashioned.jpg',
    'Martini': 'assets/images/martini.jpg',
    'Daiquiri': 'assets/images/daiquiri.jpg',
    'Sidecar': 'assets/images/sidecar.jpg',
    'Whisky Highball': 'assets/images/highball.jpg',
    'Flip': 'assets/images/flip.jpg',
  };

  _CarouselWithIndicatorState(
    this.title,
    this.credit,
    this.ingredients,
    this.predictions,
  );

  /*
  @override
  void didChangeDependencies(){
    images.forEach((key, value) => precacheImage(value.image, context));
    super.didChangeDependencies();
  }*/

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
                          minWidth: MediaQuery.of(context).size.width * .8,
                          maxWidth: MediaQuery.of(context).size.width * .9,
                        ),
                        color: Colors.black,
                        child: FittedBox(
                          alignment: Alignment.center,
                          child: Image.asset(
                            images[item[0]],
                            width: 300,
                            height: 520,
                          ),
                          fit: BoxFit.fitWidth,
                          clipBehavior: Clip.hardEdge,
                        ),
                      ),
                      //images[item[0]], //precache didn't help?
                      /*Image.asset(
                        images[item[0]],
                        width: 300,
                        fit: BoxFit.fitHeight,
                      ),*/
                      Container(
                        padding: EdgeInsets.symmetric(
                            vertical: 10.0, horizontal: 10.0),
                        child: Text(
                          item[1],
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 20 +
                                50.0 *
                                    double.parse(item[1]
                                        .substring(0, item[1].length - 1)) /
                                    100,
                          ),
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
                                Color.fromARGB(255, 0, 0, 0),
                                Color.fromARGB(0, 0, 0, 0)
                              ],
                              begin: Alignment.bottomCenter,
                              end: Alignment.topCenter,
                            ),
                          ),
                          padding: EdgeInsets.symmetric(
                              vertical: 10.0, horizontal: 10.0),
                          child: Text(
                            item[0],
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 30.0,
                              //fontWeight: FontWeight.bold,
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
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            title,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.headline2,
          ),
          SizedBox(height: 10),
          Text(
            credit,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.headline5,
          ),
          SizedBox(height: 5),
          Expanded(
            child: CarouselSlider(
              items: imageSliders,
              options: CarouselOptions(
                  autoPlay: false,
                  enlargeCenterPage: true,
                  aspectRatio: 1.0,
                  onPageChanged: (index, reason) {
                    setState(() {
                      _current = index;
                    });
                  }),
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: predictions.map((url) {
              int index = predictions.indexOf(url);
              return Container(
                width: 8.0,
                height: 8.0,
                margin:
                    EdgeInsets.symmetric(vertical: 10.0, horizontal: 2.0),
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
