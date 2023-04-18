import src.insert_frame as inserter


def single_image_example():

    ri = inserter.SimpleRifeInserter(gpuid=0)
    ri.set_verbose(True)

    prefix = "./sample_images/single_image_interpolation/"
    out_file = "./sample_workspace/single_image_interpolation/out.jpg"

    ri.interpolate_image_single(prefix + "1.jpg", prefix + "2.jpg", out_file)


def multiple_image_example():
    sample_folder = "./sample_images/multiple_image_interpolation/"
    working_folder = "./sample_workspace/multiple_image_interpolation/"

    ri = inserter.SimpleRifeInserter(tta_mode=False, uhd_mode=True)
    ri.set_verbose(True)

    # define the images with their repespetive index we want this to be inflated to 10 images (see indices)
    start = [sample_folder + "0.jpg", 0]
    end = [sample_folder + "1.jpg", 10]

    ri.interpolate_image_multiple(start, end, working_folder)


def increase_fps_example():

    ri = inserter.SimpleRifeInserter()
    ri.set_verbose(True)

    input_folder = "./sample_images/increase_fps/"
    working_folder = "./sample_workspace/increase_fps/"
    increase_factor = 100

    # start recursivly interpolating
    ri.increase_fps(input_folder, ".jpg",
                    increase_factor, working_folder)


if __name__ == '__main__':
    '''main function'''

    # single_image_example()

    multiple_image_example()

    # increase_fps_example()

    print("examples finished! See folder 'sample_workspace' for results")
