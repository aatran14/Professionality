import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import {useState} from 'react';

const responsive = {
  desktop: {
    breakpoint: { max: 3000, min: 1024 },
    items: 1,
    slidesToSlide: 1 // optional, default to 1.
  },
  tablet: {
    breakpoint: { max: 1024, min: 464 },
    items: 1,
    slidesToSlide: 1 // optional, default to 1.
  },
  mobile: {
    breakpoint: { max: 464, min: 0 },
    items: 1,
    slidesToSlide: 1 // optional, default to 1.
  }
};

export default function QuoteCarousel(props) {

    return (
        <div className="Quote-Carousel">
          <div>
        <Carousel
arrows={true}
        swipeable={true}
            draggable={true}
            showDots={false}
        centerMode={false}
  responsive={responsive}
  ssr={true} // means to render carousel on server-side.
  infinite={true}
  autoPlay={false}
//   autoPlay={props.deviceType !== "mobile" ? true : false}
  autoPlaySpeed={1000}
  keyBoardControl={true}
  customTransition="transform 1000ms ease-in-out"
  transitionDuration={1000}
  containerClass="carousel-container"
//   removeArrowOnDeviceType={["tablet", "mobile"]}
    deviceType={props.deviceType}

  dotListClass="react-multi-carousel-dot-list"
  itemClass="carousel-item-padding-0-px"
  className="blog-giant-carousel1"
>

<div className="blog-carousel-images">
<p className="words">
    "Enabling underrepresented communities is one of the most interesting challenges in the world.
     <span className="ProFresh"><b> ProFresh</b></span> helps people who change the world change the world."</p>
    <p className="author">
    - Andy Tran Co-Founder
    </p>
  </div>
  <div className="blog-carousel-images">
<p className="words">
    Our students use <span className="ProFresh"><b> ProFresh</b></span> because it <b>instantly</b> enables a form of change that they otherwise wouldn't have the resources to do.</p>
    <p className="author">
    - Teacher
    </p>
    </div>
</Carousel>
</div>

</div>
    )
}