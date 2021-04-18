---
title: Reducing R.I.S.C.
---

<h2 align="center">Can Machine Learning Help A Restaurant Group Reduce "Order Risk" For Each Patron Through Personalization?</h2>

The actual web app cannot be released publicly yet, but you can check out the demonstrator through the link below. Despite the title and credit fields working as expected, the demonstrator will only return predictions for the *Golden Boy* (public release approved by author).

<p style="font-size: 25px; text-align:center">
    <a href="demo/">
        Demo App
    </a>
</p>

The mobile app is also private for the moment. See [this page](animations/) for animations of the app in action.

### Road Map
- [x] GCP Dataflow + GCP Cloud Vision text extraction
- [x] Multinomial NLP classification
- [x] GCP Cloud Function + Flask RESTful API creation
- [x] Flutter interface
- [ ] Redshift integration for analytics (mid April '21)
- [ ] TensorFlow LSTM Network classification (late April '21)
- [ ] Refactor to AWS EC2/Fargate (early May '21)
- [ ] Pytest additions (ongoing)

This page is under construction; last updated 4/21/21.