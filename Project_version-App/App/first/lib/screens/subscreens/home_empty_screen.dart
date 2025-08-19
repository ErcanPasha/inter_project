import 'package:flutter/material.dart';

class HomeEmptyScreen extends StatefulWidget {
  const HomeEmptyScreen({super.key});

  @override
  State<HomeEmptyScreen> createState() => _HomeEmptyScreenState();
}

class _HomeEmptyScreenState extends State<HomeEmptyScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _animation = Tween<double>(begin: 0.3, end: 1.0).animate(_controller);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const logoPath = "assets/images/sixfab_logo.png";

    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          FadeTransition(
            opacity: _animation,
            child: const Image(image: AssetImage(logoPath), width: 200),
          ),
          const SizedBox(height: 20),
          Text(
            "To view the stops' states add them",
            style: TextStyle(
              color: Colors.brown.shade400,
              fontStyle: FontStyle.italic,
            ),
          ),
        ],
      ),
    );
  }
}
