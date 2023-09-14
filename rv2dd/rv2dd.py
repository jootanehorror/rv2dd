from scipy.stats import rv_discrete
import numpy as np
from typing import List, Union, Tuple, Optional, Callable



class rv_two_dimensional_discrete():
    def __init__(self, value: Union[np.ndarray, List], conditional: Optional[Callable] = None,conditional_type:Optional[str]=None):
        """
        :param value: Two-dimensional array of values and corresponding probabilities.
        :param conditional: Conditional function that takes a two-dimensional value and returns a boolean value.
        :param conditional_type:Condition on 'X' or 'Y'
        example lambda x: x[0] + x[1] > 0
        :return: None
        """
        self.values = np.array(value[0])
        self.P = value[1]
        self.XY = rv_discrete(values=(np.array([i for i in range(len(value[0]))]), value[1]))
        self.X = self._get_rv_discrete(name="x")
        self.Y = self._get_rv_discrete(name="y")
        self.conditional = conditional
        self.conditional_type=conditional_type
        self.conditional_distribution = self._get_conditional_distribution() if conditional is not None else None

    def _get_conditional_distribution(self):
        """
        :return: Conditional distribution according to the specified conditional function.
        """
        if self.conditional_type=="X":
            mark=0
        else:
            mark=1
        bool_values = np.apply_along_axis(self.conditional, 1, self.values)
        values = self.values[bool_values][:, mark]
        p = self.P[bool_values]
        p = 1 / np.sum(p) * p
        return rv_discrete(values=(values, p), name="conditional_distribution")

    def conditional_mean(self) -> np.float64:
        """
        :return: Conditional mean value.
        """
        return self.conditional_distribution.mean()

    def conditional_var(self) -> np.float64:
        """
        :return: Conditional variance.
        """
        return self.conditional_distribution.var()

    def conditional_stats(self) -> Tuple[np.float64, np.float64]:
        """
        :return: Statistical properties of the conditional distribution.
        """
        return self.conditional_distribution.stats()

    def mean(self) -> Tuple[np.float64, np.float64]:
        """
        :return: Mean value for X and Y.
        """
        return (self.X.mean(), self.Y.mean())

    def var(self) -> Tuple[np.float64, np.float64]:
        """
          :return: Variance value for X and Y.
          """
        return (self.X.var(), self.Y.var())

    def stats(self) -> Tuple[Tuple[np.float64, np.float64], Tuple[np.float64, np.float64]]:
        """
        :return: Statistical properties for X and Y.
        """
        return (self.X.stats(), self.Y.stats())

    def rvs(self, size: int = 1) -> np.ndarray:
        """
        :param size: Sample size.
        :return: Random values from the two-dimensional discrete distribution.
        """
        voc = []
        indexes = self.XY.rvs(size=size)
        for i in indexes:
            voc.append(self.values[i])
        return np.array(voc)

    def cdf(self, x: Optional[Union[int, float]] = None, y: Optional[Union[int, float]] = None,
            conditional: bool = False) -> np.float64:
        """
        :param x: Value on the X axis.
        :param y: Value on the Y axis.
        :param conditional: Conditional or unconditional distribution.
        :return: CDF (Cumulative Distribution Function) value at point (x, y) or conditional (x, y).
        """
        if conditional:
            return np.sum(np.apply_along_axis(self.conditional, 1, self.values) * self.P)
        elif x is not None and y is not None:
            return np.sum((self.values[:, 0] <= x) * (self.values[:, 1] <= y) * self.P)
        elif x is None and y is not None:
            return self.Y.cdf(y)
        elif y is None and x is not None:
            return self.X.cdf(x)

    def _get_rv_discrete(self, name="x"):
        """
        :param name: Name of the random variable (X or Y).
        :return: Discrete distribution based on values along the specified axis.
        """
        if name == "x":
            mark = 0
        else:
            mark = 1
        x_ = []
        x_p = []
        for i in self.values:
            x_.append(i[mark])
        x_ = np.array(x_)
        for i in np.unique(x_):
            p_k = 0
            for j in np.where(x_ == i)[0]:
                p_k += self.P[j]
            x_p.append(p_k)
        return rv_discrete(name=name, values=(np.unique(x_), x_p))
