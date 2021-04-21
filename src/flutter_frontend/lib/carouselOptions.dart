import 'package:flutter/material.dart';

enum CarouselPageChangedReason { timed, manual, controller }

enum CenterPageEnlargeStrategy { scale, height }

class CarouselOptions {
  final double height;
  final double aspectRatio;
  final double viewportFraction;
  final int initialPage;
  final bool enableInfiniteScroll;
  final bool reverse;
  final bool autoPlay;
  final Duration autoPlayInterval;
  final Duration autoPlayAnimationDuration;
  final Curve autoPlayCurve;
  final bool enlargeCenterPage;
  final Axis scrollDirection;
  final Function(int index, CarouselPageChangedReason reason) onPageChanged;
  final ValueChanged<double> onScrolled;
  final ScrollPhysics scrollPhysics;
  final bool pageSnapping;
  final bool pauseAutoPlayOnTouch;
  final bool pauseAutoPlayOnManualNavigate;
  final bool pauseAutoPlayInFiniteScroll;
  final PageStorageKey pageViewKey;
  final CenterPageEnlargeStrategy enlargeStrategy;
  final bool disableCenter;

  CarouselOptions({
    this.height,
    this.aspectRatio: 16 / 9,
    this.viewportFraction: 0.8,
    this.initialPage: 0,
    this.enableInfiniteScroll: true,
    this.reverse: false,
    this.autoPlay: false,
    this.autoPlayInterval: const Duration(seconds: 4),
    this.autoPlayAnimationDuration = const Duration(milliseconds: 800),
    this.autoPlayCurve: Curves.fastOutSlowIn,
    this.enlargeCenterPage = false,
    this.onPageChanged,
    this.onScrolled,
    this.scrollPhysics,
    this.pageSnapping = true,
    this.scrollDirection: Axis.horizontal,
    this.pauseAutoPlayOnTouch: true,
    this.pauseAutoPlayOnManualNavigate: true,
    this.pauseAutoPlayInFiniteScroll: false,
    this.pageViewKey,
    this.enlargeStrategy: CenterPageEnlargeStrategy.scale,
    this.disableCenter: false,
  });
}
