import 'dart:developer';
import 'dart:convert';
import 'package:http/http.dart' as http;

import 'package:flutter/material.dart';

import 'predictionScreen.dart';

class InputScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      //backgroundColor: Colors.grey[900],
      body: Center(
        child: SizedBox(
          width: 400,
          child: Card(
            child: InputForm(),
          ),
        ),
      ),
    );
  }
}

class InputForm extends StatefulWidget {
  @override
  _InputFormState createState() => _InputFormState();
}

class _InputFormState extends State<InputForm> {
  final _titleTextController = TextEditingController();
  final _creditTextController = TextEditingController();
  final _ingredientsTextController = TextEditingController();

  double _formProgress = 0;

  void _updateFormProgress() {
    var progress = 0.0;
    final controllers = [
      _titleTextController,
      _creditTextController,
      _ingredientsTextController,
    ];
    for (final controller in controllers) {
      if (controller.value.text.isNotEmpty) {
        progress += 1 / controllers.length;
      }
    }
    setState(() {
      _formProgress = progress;
    });
  }

  Future<void> _showMyDialog(String content) async {

    return showDialog<void>(
      context: context,
      barrierDismissible: false, // user must tap button!
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('AlertDialog Title'),
          content: SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                Text(content),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: Text('Dismiss'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _showPredictionScreen() async {
    var answer = await fetchFromFlask("chocolate milk");
    await _showMyDialog('$answer');
    log('after cors got ${answer}');
    /*
        Navigator.of(context).pushNamed(
            PredictionScreen.routeName,
            arguments: ScreenArguments(
                _titleTextController.text,
                _creditTextController.text,
                _ingredientsTextController.text,
                await fetchFromFlask("chocolate milk"),
            ),
        );*/
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      onChanged: _updateFormProgress,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          AnimatedProgressIndicator(value: _formProgress),
          Text('Enter a Cocktail',
              style: Theme.of(context).textTheme.headline4),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Tooltip(
              message: 'like "Arnold Palmer"',
              child: TextFormField(
                controller: _titleTextController,
                decoration: InputDecoration(
                  labelText: 'Enter recipe title',
                ),
                cursorColor: Theme.of(context).accentColor,
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Tooltip(
              message: 'like "Difford\'s Guide"',
              child: TextFormField(
                controller: _creditTextController,
                decoration: InputDecoration(
                  labelText: 'Enter recipe origin',
                ),
                cursorColor: Theme.of(context).accentColor,
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Tooltip(
              message: 'like "3 ounces black tea 2 ounces lemon juice 1 '
                  'ounce rich syrup"',
              child: TextFormField(
                controller: _ingredientsTextController,
                decoration: InputDecoration(
                  labelText: 'Enter Ingredients',
                ),
                cursorColor: Theme.of(context).accentColor,
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextButton(
              onPressed: _formProgress == 1 ? _showPredictionScreen : null,
              child: Text(
                'Classify',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              style: ButtonStyle(
                padding:
                    MaterialStateProperty.all<EdgeInsets>(EdgeInsets.all(15)),
                foregroundColor: MaterialStateProperty.resolveWith(
                    (Set<MaterialState> states) {
                  return states.contains(MaterialState.disabled)
                      ? null
                      : Colors.black;
                }),
                backgroundColor: MaterialStateProperty.resolveWith(
                    (Set<MaterialState> states) {
                  return states.contains(MaterialState.disabled)
                      ? null
                      : Theme.of(context).accentColor;
                }),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class AnimatedProgressIndicator extends StatefulWidget {
  final double value;

  AnimatedProgressIndicator({
    @required this.value,
  });

  @override
  State<StatefulWidget> createState() {
    return _AnimatedProgressIndicatorState();
  }
}

class _AnimatedProgressIndicatorState extends State<AnimatedProgressIndicator>
    with SingleTickerProviderStateMixin {
  AnimationController _controller;
  Animation<Color> _colorAnimation;
  Animation<double> _curveAnimation;

  void initState() {
    super.initState();
    _controller = AnimationController(
        duration: Duration(milliseconds: 1200), vsync: this);

    final colorTween = TweenSequence([
      TweenSequenceItem(
        tween: ColorTween(begin: Colors.red, end: Colors.orange),
        weight: 1,
      ),
      TweenSequenceItem(
        tween: ColorTween(begin: Colors.orange, end: Colors.yellow),
        weight: 1,
      ),
      TweenSequenceItem(
        tween: ColorTween(begin: Colors.yellow, end: Colors.green),
        weight: 1,
      ),
    ]);

    _colorAnimation = _controller.drive(colorTween);
    _curveAnimation = _controller.drive(CurveTween(curve: Curves.easeIn));
  }

  void didUpdateWidget(oldWidget) {
    super.didUpdateWidget(oldWidget);
    _controller.animateTo(widget.value);
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) => LinearProgressIndicator(
        value: _curveAnimation.value,
        valueColor: _colorAnimation,
        backgroundColor: _colorAnimation.value?.withOpacity(0.4),
      ),
    );
  }
}

class ScreenArguments {
  final String title;
  final String credit;
  final String ingredients;
  final List<String> predictions;

  ScreenArguments(
    this.title,
    this.credit,
    this.ingredients,
    this.predictions,
  );
}

Future<List> fetchFromFlask(String toSend) async {
  log('pre-fetch');
  try {
    final response = await http.post(
      Uri.https(//'jsonplaceholder.typicode.com', 'albums'),
          'us-central1-palates-codex.cloudfunctions.net', '/servePrediction'),
      headers: <String, String>{
        'Content-Type': 'application/json; '
            'charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'ingredients': toSend,
        //'title': toSend,
      }),
    );
    return Prediction.fromJson(jsonDecode(response.body)).predictionResponse;
  } catch (e) {
    return ['exception in dart ${e}'];
  }
  /*if (response.statusCode == 200) {
    log('was 200');
    return Prediction.fromJson(jsonDecode(response.body)).predictionResponse;
  } else {
    log('was not 200');
    throw Exception('Failed to communicate with API (${response.statusCode})');
  }*/
}

class Prediction {
  final List<List> predictionResponse;

  Prediction({this.predictionResponse});

  factory Prediction.fromJson(Map<String, dynamic> json) {
    return Prediction(
      predictionResponse:
          json.entries.map<List>((entry) => [entry.key, entry.value]).toList(),
    );
  }
}
