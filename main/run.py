from main.utils.logger import Logger
from main.utils.main_parser import MainParser
from main.directory import Directory
from main.file import File
from main.convnet import ConvNet
import logging
import os


def run_app():

    main_parser = MainParser().register_args()
    args = main_parser.parse_args()

    logger = Logger(log_level=args.verbosity)
    logger.set_log_level()

    model_dir = Directory(args.model_dir)

    if os.path.isfile(args.img_dir):
        image_dir = File(args.img_dir)
    else:
        image_dir = Directory(args.img_dir)

    img_size = 64
    channels = 3
    filter_size = 3

    if args.mode == 'train':

        if args.clean:
            model_dir.remove()

        model_dir.create()

        model = ConvNet(model_dir, image_dir, img_size, channels, filter_size, batch_size=args.batch_size)

        model.train(training_epochs=args.iterations)

    else:
        model = ConvNet(model_dir, image_dir, img_size, channels, filter_size, batch_size=1)
        predictions = model.predict()

        for prediction in predictions:
            logging.info("File: {} --- Prediction: {}".format(*prediction))


if __name__ == '__main__':

    run_app()
