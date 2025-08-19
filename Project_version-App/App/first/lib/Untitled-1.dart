import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/stop_info.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final List<StopInfo> items = [];

  String _time = "";
  String _date = "";

  @override
  void initState() {
    super.initState();
    _updateDateTime();
  }

  void _updateDateTime() {
    final now = DateTime.now();
    _time = DateFormat.Hm().format(now); // "14:58"
    _date = DateFormat("dd.MM.yyyy").format(now); // "18.08.2025"
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final double height = MediaQuery.of(context).size.height;
    final double width = MediaQuery.of(context).size.width;
    return Scaffold(
      backgroundColor: items.isEmpty ? Colors.grey.shade200 : null,
      appBar: AppBar(
        toolbarHeight: height * 0.1,
        titleSpacing: width * 0.01,
        title: Row(
          children: [
            SizedBox(width: width * 0.01),
            CircleAvatar(
              radius: 18,
              backgroundColor: Colors.grey.shade300,
              child: const Icon(Icons.person, color: Colors.black54),
            ),
            const Spacer(),
            const Text('Sixfab', style: TextStyle(fontWeight: FontWeight.w800)),
            const Spacer(),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  _time,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 2),
                Text(_date, style: const TextStyle(fontSize: 12)),
              ],
            ),
            SizedBox(width: width * 0.01),
          ],
        ),
      ),
      body: items.isEmpty
          ? const _EmptyState()
          : ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: items.length,
              itemBuilder: (context, i) => StopCard(info: items[i]),
            ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.blueGrey,
        hoverColor: Colors.cyan,
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("You are directed to Stop Page"),
              duration: Duration(milliseconds: 150),
            ),
          );
        },
        child: const Icon(Icons.add_circle_sharp),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    );
  }
}

/// ----- Empty State -----
class _EmptyState extends StatefulWidget {
  const _EmptyState();

  @override
  State<_EmptyState> createState() => _EmptyStateState();
}

class _EmptyStateState extends State<_EmptyState>
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

/// ----- Stop Card -----
class StopCard extends StatefulWidget {
  final StopInfo info;
  const StopCard({super.key, required this.info});

  @override
  State<StopCard> createState() => _StopCardState();
}

class _StopCardState extends State<StopCard> with TickerProviderStateMixin {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context).textTheme;
    final info = widget.info;

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      elevation: 0.5,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () => setState(() => _expanded = !_expanded),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(12, 10, 12, 12),
          child: Column(
            children: [
              Row(
                children: [
                  _cell(info.name, flex: 5, bold: true, t: t),
                  _cell(info.side, flex: 3, t: t),
                  _cell(info.district, flex: 3, t: t),
                  _cell(info.lastUpdate, flex: 4, alignEnd: true, t: t),
                ],
              ),
              const SizedBox(height: 8),
              Divider(height: 1, thickness: 1, color: Colors.grey.shade300),
              AnimatedSize(
                duration: const Duration(milliseconds: 220),
                curve: Curves.easeInOut,
                alignment: Alignment.topCenter,
                child: _expanded
                    ? Padding(
                        padding: const EdgeInsets.only(top: 10),
                        child: StopDetailPanel(info: info),
                      )
                    : const SizedBox.shrink(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _cell(
    String text, {
    required TextTheme t,
    int flex = 1,
    bool bold = false,
    bool alignEnd = false,
  }) {
    return Expanded(
      flex: flex,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 6),
        child: Text(
          text,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          textAlign: alignEnd ? TextAlign.right : TextAlign.left,
          style: (bold ? t.titleMedium : t.bodyMedium)?.copyWith(height: 1.1),
        ),
      ),
    );
  }
}

/// ----- Detail Panel -----
class StopDetailPanel extends StatelessWidget {
  final StopInfo info;
  const StopDetailPanel({super.key, required this.info});

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context).textTheme;

    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey.shade600),
        borderRadius: BorderRadius.circular(10),
      ),
      padding: const EdgeInsets.all(12),
      child: Column(
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: _panel(
                  title: 'Yolcu Bilgisi',
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: info.passengerSeries.isEmpty
                        ? [Text('—', style: t.bodyMedium)]
                        : info.passengerSeries
                            .map(
                              (e) => Padding(
                                padding: const EdgeInsets.symmetric(vertical: 2),
                                child: Text('${e.time}  —  ${e.count}',
                                    style: t.bodyMedium),
                              ),
                            )
                            .toList(),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _panel(
                  title: 'Gelen Otobüsler',
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: info.incomingBuses.isEmpty
                        ? [Text('—', style: t.bodyMedium)]
                        : info.incomingBuses
                            .map(
                              (b) => Padding(
                                padding:
                                    const EdgeInsets.symmetric(vertical: 2),
                                child: Text(b, style: t.bodyMedium),
                              ),
                            )
                            .toList(),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  OutlinedButton.icon(
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Veriler yenilendi (mock).'),
                        ),
                      );
                    },
                    icon: const Icon(Icons.refresh),
                    label: const Text('Yenile'),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 12),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Son 5 dakika (30 görsel) açılıyor…'),
                  ),
                );
              },
              child: const Text('Son 5 dakika (30 görsel) için tıkla'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _panel({required String title, required Widget child}) {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: Colors.green.shade300),
        borderRadius: BorderRadius.circular(8),
      ),
      padding: const EdgeInsets.all(10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontWeight: FontWeight.w700)),
          const SizedBox(height: 8),
          child,
        ],
      ),
    );
  }
}
