# coding=utf-8

from pines import metrics

def compute_split_gain_helper(args):
    split_criterion, X, y, feature_id, split_value = args
    _, _, y_left, y_right = split_dataset(X, y, feature_id, split_value)
    if len(y_left) == 0 or len(y_right) == 0:
        return None
    gain = compute_split_gain(split_criterion, y, y_left, y_right)
    return gain

def split_dataset( X, y, feature_id, value):
    mask = X[:, feature_id] <= value
    return X[mask], X[~mask], y[mask], y[~mask]

def compute_split_gain(split_criterion, y, y_left, y_right):
    splits = [y_left, y_right]
    return split_criterion(y) - \
           sum([split_criterion(split) * float(len(split))/len(y) for split in splits])

class SplitCriterion:
    GINI = 'gini'
    ENTROPY = 'entropy'
    MSE = 'mse'

    @staticmethod
    def resolve_split_criterion(criterion_name):
        if criterion_name == SplitCriterion.GINI:
            return metrics.gini_index
        elif criterion_name == SplitCriterion.ENTROPY:
            return metrics.entropy
        elif criterion_name == SplitCriterion.MSE:
            return metrics.mse
        else:
            raise ValueError('Unknown criterion {}'.format(criterion_name))