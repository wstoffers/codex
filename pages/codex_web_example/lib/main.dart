import 'package:flutter/material.dart';

void main() => runApp(SignUpApp());

class SignUpApp extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            routes: {
                '/': (context) => SignUpScreen(),
                '/welcome': (context) => WelcomeScreen(),
            },
        );
    }
}

class SignUpScreen extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            backgroundColor: Colors.grey[200],
            body: Center(
                child: SizedBox(
                    width: 400,
                    child: Card(
                        child: SignUpForm(),
                    ),
                ),
            ),
        );
    }
}

class WelcomeScreen extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            body: Center(
                child: Text('Pretend this is a %',
                            style: Theme.of(context).textTheme.headline2),
            ),
        );
    }
}

class SignUpForm extends StatefulWidget {
    @override
    _SignUpFormState createState() => _SignUpFormState();
}

class _SignUpFormState extends State<SignUpForm> {
    final _firstNameTextController = TextEditingController();
    final _lastNameTextController = TextEditingController();
    final _usernameTextController = TextEditingController();

    double _formProgress = 0;

    void _updateFormProgress() {
        var progress = 0.0;
        final controllers = [
            _firstNameTextController,
            _lastNameTextController,
            _usernameTextController
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

    void _showWelcomeScreen() {
        Navigator.of(context).pushNamed('/welcome');
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
                        child: TextFormField(
                            controller: _firstNameTextController,
                            decoration: InputDecoration(hintText: 'Type in '
                                                                  'core '
                                                                  'ingredient'),
                        ),
                    ),
                    Padding(
                        padding: EdgeInsets.all(8.0),
                        child: TextFormField(
                            controller: _lastNameTextController,
                            decoration: InputDecoration(hintText: 'Type in '
                                                                  'balance '
                                                                  'ingredient'),
                        ),
                    ),
                    Padding(
                        padding: EdgeInsets.all(8.0),
                        child: TextFormField(
                            controller: _usernameTextController,
                            decoration: InputDecoration(hintText: 'Type in '
                                                                  'seasoning '
                                                                  'ingredient'),
                        ),
                    ),
                    TextButton(
                        style: ButtonStyle(
                            padding: MaterialStateProperty.all<EdgeInsets>(
                                EdgeInsets.all(20)
                            ),
                            foregroundColor: MaterialStateProperty.resolveWith(
                                (Set<MaterialState> states) {
                                return states.contains(MaterialState.disabled) ?
                                           null : Colors.white;
                                }
                            ),
                            backgroundColor: MaterialStateProperty.resolveWith(
                                (Set<MaterialState> states) {
                                return states.contains(MaterialState.disabled) ?
                                           null : Colors.blue;
                                }
                            ),
                        ),
                        onPressed: _formProgress == 1 ?
                                       _showWelcomeScreen : null,
                        child: Text('Check Family'),
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
            _curveAnimation = _controller.drive(
                                  CurveTween(curve: Curves.easeIn));
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