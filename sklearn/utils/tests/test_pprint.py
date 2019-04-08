import re
from pprint import PrettyPrinter

import numpy as np

from sklearn.utils._pprint import _EstimatorPrettyPrinter
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import set_config


# Ignore flake8 (lots of line too long issues)
# flake8: noqa

# Constructors excerpted to test pprinting
class LogisticRegression(BaseEstimator):
    def __init__(self, penalty='l2', dual=False, tol=1e-4, C=1.0,
                 fit_intercept=True, intercept_scaling=1, class_weight=None,
                 random_state=None, solver='warn', max_iter=100,
                 multi_class='warn', verbose=0, warm_start=False, n_jobs=None,
                 l1_ratio=None):
        self.penalty = penalty
        self.dual = dual
        self.tol = tol
        self.C = C
        self.fit_intercept = fit_intercept
        self.intercept_scaling = intercept_scaling
        self.class_weight = class_weight
        self.random_state = random_state
        self.solver = solver
        self.max_iter = max_iter
        self.multi_class = multi_class
        self.verbose = verbose
        self.warm_start = warm_start
        self.n_jobs = n_jobs
        self.l1_ratio = l1_ratio

    def fit(self, X, y):
        return self


class StandardScaler(BaseEstimator, TransformerMixin):
    def __init__(self, copy=True, with_mean=True, with_std=True):
        self.with_mean = with_mean
        self.with_std = with_std
        self.copy = copy

    def transform(self, X, copy=None):
        return self


class RFE(BaseEstimator):
    def __init__(self, estimator, n_features_to_select=None, step=1,
                 verbose=0):
        self.estimator = estimator
        self.n_features_to_select = n_features_to_select
        self.step = step
        self.verbose = verbose


class GridSearchCV(BaseEstimator):
    def __init__(self, estimator, param_grid, scoring=None,
                 n_jobs=None, iid='warn', refit=True, cv='warn', verbose=0,
                 pre_dispatch='2*n_jobs', error_score='raise-deprecating',
                 return_train_score=False):
        self.estimator = estimator
        self.param_grid = param_grid
        self.scoring = scoring
        self.n_jobs = n_jobs
        self.iid = iid
        self.refit = refit
        self.cv = cv
        self.verbose = verbose
        self.pre_dispatch = pre_dispatch
        self.error_score = error_score
        self.return_train_score = return_train_score


class CountVectorizer(BaseEstimator):
    def __init__(self, input='content', encoding='utf-8',
                 decode_error='strict', strip_accents=None,
                 lowercase=True, preprocessor=None, tokenizer=None,
                 stop_words=None, token_pattern=r"(?u)\b\w\w+\b",
                 ngram_range=(1, 1), analyzer='word',
                 max_df=1.0, min_df=1, max_features=None,
                 vocabulary=None, binary=False, dtype=np.int64):
        self.input = input
        self.encoding = encoding
        self.decode_error = decode_error
        self.strip_accents = strip_accents
        self.preprocessor = preprocessor
        self.tokenizer = tokenizer
        self.analyzer = analyzer
        self.lowercase = lowercase
        self.token_pattern = token_pattern
        self.stop_words = stop_words
        self.max_df = max_df
        self.min_df = min_df
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vocabulary = vocabulary
        self.binary = binary
        self.dtype = dtype


class Pipeline(BaseEstimator):
    def __init__(self, steps, memory=None):
        self.steps = steps
        self.memory = memory


class PCA(BaseEstimator):
    def __init__(self, n_components=None, copy=True, whiten=False,
                 svd_solver='auto', tol=0.0, iterated_power='auto',
                 random_state=None):
        self.n_components = n_components
        self.copy = copy
        self.whiten = whiten
        self.svd_solver = svd_solver
        self.tol = tol
        self.iterated_power = iterated_power
        self.random_state = random_state


class NMF(BaseEstimator):
    def __init__(self, n_components=None, init=None, solver='cd',
                 beta_loss='frobenius', tol=1e-4, max_iter=200,
                 random_state=None, alpha=0., l1_ratio=0., verbose=0,
                 shuffle=False):
        self.n_components = n_components
        self.init = init
        self.solver = solver
        self.beta_loss = beta_loss
        self.tol = tol
        self.max_iter = max_iter
        self.random_state = random_state
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.verbose = verbose
        self.shuffle = shuffle


class SimpleImputer(BaseEstimator):
    def __init__(self, missing_values=np.nan, strategy="mean",
                 fill_value=None, verbose=0, copy=True):
        self.missing_values = missing_values
        self.strategy = strategy
        self.fill_value = fill_value
        self.verbose = verbose
        self.copy = copy


def test_basic():
    # Basic pprint test
    lr = LogisticRegression()
    expected = """
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='warn', n_jobs=None, penalty='l2',
                   random_state=None, solver='warn', tol=0.0001, verbose=0,
                   warm_start=False)"""

    expected = expected[1:]  # remove first \n
    assert lr.__repr__() == expected


def test_changed_only():
    # Make sure the changed_only param is correctly used
    set_config(print_changed_only=True)
    lr = LogisticRegression(C=99)
    expected = """LogisticRegression(C=99)"""
    assert lr.__repr__() == expected

    # Check with a repr that doesn't fit on a single line
    lr = LogisticRegression(C=99, class_weight=.4, fit_intercept=False,
                            tol=1234, verbose=True)
    expected = """
LogisticRegression(C=99, class_weight=0.4, fit_intercept=False, tol=1234,
                   verbose=True)"""
    expected = expected[1:]  # remove first \n
    assert lr.__repr__() == expected

    imputer = SimpleImputer(missing_values=0)
    expected = """SimpleImputer(missing_values=0)"""
    assert imputer.__repr__() == expected

    # Defaults to np.NaN, trying with float('NaN')
    imputer = SimpleImputer(missing_values=float('NaN'))
    expected = """SimpleImputer()"""
    assert imputer.__repr__() == expected

    set_config(print_changed_only=False)


def test_pipeline():
    # Render a pipeline object
    pipeline = make_pipeline(StandardScaler(), LogisticRegression(C=999))
    expected = """
Pipeline(memory=None,
         steps=[('standardscaler',
                 StandardScaler(copy=True, with_mean=True, with_std=True)),
                ('logisticregression',
                 LogisticRegression(C=999, class_weight=None, dual=False,
                                    fit_intercept=True, intercept_scaling=1,
                                    l1_ratio=None, max_iter=100,
                                    multi_class='warn', n_jobs=None,
                                    penalty='l2', random_state=None,
                                    solver='warn', tol=0.0001, verbose=0,
                                    warm_start=False))])"""

    expected = expected[1:]  # remove first \n
    assert pipeline.__repr__() == expected


def test_deeply_nested():
    # Render a deeply nested estimator
    rfe = RFE(RFE(RFE(RFE(RFE(RFE(RFE(LogisticRegression())))))))
    expected = """
RFE(estimator=RFE(estimator=RFE(estimator=RFE(estimator=RFE(estimator=RFE(estimator=RFE(estimator=LogisticRegression(C=1.0,
                                                                                                                     class_weight=None,
                                                                                                                     dual=False,
                                                                                                                     fit_intercept=True,
                                                                                                                     intercept_scaling=1,
                                                                                                                     l1_ratio=None,
                                                                                                                     max_iter=100,
                                                                                                                     multi_class='warn',
                                                                                                                     n_jobs=None,
                                                                                                                     penalty='l2',
                                                                                                                     random_state=None,
                                                                                                                     solver='warn',
                                                                                                                     tol=0.0001,
                                                                                                                     verbose=0,
                                                                                                                     warm_start=False),
                                                                                        n_features_to_select=None,
                                                                                        step=1,
                                                                                        verbose=0),
                                                                          n_features_to_select=None,
                                                                          step=1,
                                                                          verbose=0),
                                                            n_features_to_select=None,
                                                            step=1, verbose=0),
                                              n_features_to_select=None, step=1,
                                              verbose=0),
                                n_features_to_select=None, step=1, verbose=0),
                  n_features_to_select=None, step=1, verbose=0),
    n_features_to_select=None, step=1, verbose=0)"""

    expected = expected[1:]  # remove first \n
    assert rfe.__repr__() == expected


def test_gridsearch():
    # render a gridsearch
    param_grid = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                   'C': [1, 10, 100, 1000]},
                  {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    gs = GridSearchCV(SVC(), param_grid, cv=5)

    expected = """
GridSearchCV(cv=5, error_score='raise-deprecating',
             estimator=SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
                           decision_function_shape='ovr', degree=3,
                           gamma='auto_deprecated', kernel='rbf', max_iter=-1,
                           probability=False, random_state=None, shrinking=True,
                           tol=0.001, verbose=False),
             iid='warn', n_jobs=None,
             param_grid=[{'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001],
                          'kernel': ['rbf']},
                         {'C': [1, 10, 100, 1000], 'kernel': ['linear']}],
             pre_dispatch='2*n_jobs', refit=True, return_train_score=False,
             scoring=None, verbose=0)"""

    expected = expected[1:]  # remove first \n
    assert gs.__repr__() == expected


def test_gridsearch_pipeline():
    # render a pipeline inside a gridsearch
    pp = _EstimatorPrettyPrinter(compact=True, indent=1, indent_at_name=True)

    pipeline = Pipeline([
        ('reduce_dim', PCA()),
        ('classify', LinearSVC())
    ])
    N_FEATURES_OPTIONS = [2, 4, 8]
    C_OPTIONS = [1, 10, 100, 1000]
    param_grid = [
        {
            'reduce_dim': [PCA(iterated_power=7), NMF()],
            'reduce_dim__n_components': N_FEATURES_OPTIONS,
            'classify__C': C_OPTIONS
        },
        {
            'reduce_dim': [SelectKBest(chi2)],
            'reduce_dim__k': N_FEATURES_OPTIONS,
            'classify__C': C_OPTIONS
        }
    ]
    gspipline = GridSearchCV(pipeline, cv=3, n_jobs=1, param_grid=param_grid)
    expected = """
GridSearchCV(cv=3, error_score='raise-deprecating',
             estimator=Pipeline(memory=None,
                                steps=[('reduce_dim',
                                        PCA(copy=True, iterated_power='auto',
                                            n_components=None,
                                            random_state=None,
                                            svd_solver='auto', tol=0.0,
                                            whiten=False)),
                                       ('classify',
                                        LinearSVC(C=1.0, class_weight=None,
                                                  dual=True, fit_intercept=True,
                                                  intercept_scaling=1,
                                                  loss='squared_hinge',
                                                  max_iter=1000,
                                                  multi_class='ovr',
                                                  penalty='l2',
                                                  random_state=None, tol=0.0001,
                                                  verbose=0))]),
             iid='warn', n_jobs=1,
             param_grid=[{'classify__C': [1, 10, 100, 1000],
                          'reduce_dim': [PCA(copy=True, iterated_power=7,
                                             n_components=None,
                                             random_state=None,
                                             svd_solver='auto', tol=0.0,
                                             whiten=False),
                                         NMF(alpha=0.0, beta_loss='frobenius',
                                             init=None, l1_ratio=0.0,
                                             max_iter=200, n_components=None,
                                             random_state=None, shuffle=False,
                                             solver='cd', tol=0.0001,
                                             verbose=0)],
                          'reduce_dim__n_components': [2, 4, 8]},
                         {'classify__C': [1, 10, 100, 1000],
                          'reduce_dim': [SelectKBest(k=10,
                                                     score_func=<function chi2 at some_address>)],
                          'reduce_dim__k': [2, 4, 8]}],
             pre_dispatch='2*n_jobs', refit=True, return_train_score=False,
             scoring=None, verbose=0)"""

    expected = expected[1:]  # remove first \n
    repr_ = pp.pformat(gspipline)
    # Remove address of '<function chi2 at 0x.....>' for reproducibility
    repr_ = re.sub('function chi2 at 0x.*>',
                   'function chi2 at some_address>', repr_)
    assert repr_ == expected

def test_n_max_elements_to_show():

    n_max_elements_to_show = 30
    pp = _EstimatorPrettyPrinter(
        compact=True, indent=1, indent_at_name=True,
        n_max_elements_to_show=n_max_elements_to_show
    )

    # No ellipsis
    vocabulary = {i: i for i in range(n_max_elements_to_show)}
    vectorizer = CountVectorizer(vocabulary=vocabulary)

    expected = r"""
CountVectorizer(analyzer='word', binary=False, decode_error='strict',
                dtype=<class 'numpy.int64'>, encoding='utf-8', input='content',
                lowercase=True, max_df=1.0, max_features=None, min_df=1,
                ngram_range=(1, 1), preprocessor=None, stop_words=None,
                strip_accents=None, token_pattern='(?u)\\b\\w\\w+\\b',
                tokenizer=None,
                vocabulary={0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
                            8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14,
                            15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20,
                            21: 21, 22: 22, 23: 23, 24: 24, 25: 25, 26: 26,
                            27: 27, 28: 28, 29: 29})"""

    expected = expected[1:]  # remove first \n
    assert  pp.pformat(vectorizer) == expected

    # Now with ellipsis
    vocabulary = {i: i for i in range(n_max_elements_to_show + 1)}
    vectorizer = CountVectorizer(vocabulary=vocabulary)

    expected = r"""
CountVectorizer(analyzer='word', binary=False, decode_error='strict',
                dtype=<class 'numpy.int64'>, encoding='utf-8', input='content',
                lowercase=True, max_df=1.0, max_features=None, min_df=1,
                ngram_range=(1, 1), preprocessor=None, stop_words=None,
                strip_accents=None, token_pattern='(?u)\\b\\w\\w+\\b',
                tokenizer=None,
                vocabulary={0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
                            8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14,
                            15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20,
                            21: 21, 22: 22, 23: 23, 24: 24, 25: 25, 26: 26,
                            27: 27, 28: 28, 29: 29, ...})"""

    expected = expected[1:]  # remove first \n
    assert  pp.pformat(vectorizer) == expected

    # Also test with lists
    param_grid = {'C': list(range(n_max_elements_to_show))}
    gs = GridSearchCV(SVC(), param_grid)
    expected = """
GridSearchCV(cv='warn', error_score='raise-deprecating',
             estimator=SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
                           decision_function_shape='ovr', degree=3,
                           gamma='auto_deprecated', kernel='rbf', max_iter=-1,
                           probability=False, random_state=None, shrinking=True,
                           tol=0.001, verbose=False),
             iid='warn', n_jobs=None,
             param_grid={'C': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                               15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                               27, 28, 29]},
             pre_dispatch='2*n_jobs', refit=True, return_train_score=False,
             scoring=None, verbose=0)"""

    expected = expected[1:]  # remove first \n
    assert  pp.pformat(gs) == expected

    # Now with ellipsis
    param_grid = {'C': list(range(n_max_elements_to_show + 1))}
    gs = GridSearchCV(SVC(), param_grid)
    expected = """
GridSearchCV(cv='warn', error_score='raise-deprecating',
             estimator=SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
                           decision_function_shape='ovr', degree=3,
                           gamma='auto_deprecated', kernel='rbf', max_iter=-1,
                           probability=False, random_state=None, shrinking=True,
                           tol=0.001, verbose=False),
             iid='warn', n_jobs=None,
             param_grid={'C': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                               15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                               27, 28, 29, ...]},
             pre_dispatch='2*n_jobs', refit=True, return_train_score=False,
             scoring=None, verbose=0)"""

    expected = expected[1:]  # remove first \n
    assert  pp.pformat(gs) == expected


def test_length_constraint():
    # When repr is still too long, use bruteforce ellipsis
    # repr is a very long line so we don't check for equality here, just that
    # ellipsis has been done. It's not the ellipsis from before because the
    # number of elements in the dict is only 1.
    vocabulary = {0: 'hello' * 1000}
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    repr_ = vectorizer.__repr__()
    assert '...' in repr_


def test_builtin_prettyprinter():
    # non regression test than ensures we can still use the builtin
    # PrettyPrinter class for estimators (as done e.g. by joblib).
    # Used to be a bug

    PrettyPrinter().pprint(LogisticRegression())
