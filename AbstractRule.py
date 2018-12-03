import abc


class AbstractRule(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def isContainingDrumFill(self,bar):
        pass


    
