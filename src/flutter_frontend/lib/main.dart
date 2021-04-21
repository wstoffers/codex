import 'dart:developer';

import 'package:flutter/material.dart';

import 'inputScreen.dart';
import 'predictionScreen.dart';

void main() {
  runApp(CodexApp());
}

class CodexApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        brightness: Brightness.dark,
        accentColor: Colors.orange,
      ),
      routes: {
        '/': (context) => InputScreen(),
      },
      onGenerateRoute: (settings) {
        if (settings.name == PredictionScreen.routeName) {
          final ScreenArguments args = settings.arguments as ScreenArguments;
          return MaterialPageRoute(
            builder: (context) {
              return PredictionScreen(
                title: args.title,
                credit: args.credit,
                ingredients: args.ingredients,
                predictions: args.predictions,
              );
            },
          );
        }
        log('main page hit what is probably else, returning null');
        return null;
      },
    );
  }
}
