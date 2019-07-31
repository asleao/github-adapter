import threading
import time
import pika
from .controller import setup, callback_repository,callback_collaborator


class Consumer(object):
    """ Background thread for consuming queues
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self):
        """ Constructor
        """

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        params_amq = setup()
        connection = pika.BlockingConnection(params_amq)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='Github_Repository')
        channel.queue_declare(queue='Github_Collaborator')
        channel.basic_consume(callback_repository,
                              queue='Github_Repository',
                              no_ack=True)
        channel.basic_consume(callback_collaborator,
                              queue='Github_Collaborator',
                              no_ack=True)                    
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

        connection.close()
