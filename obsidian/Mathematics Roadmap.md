# A mathematical roadmap for quantum chemistry

This text accompanies the [[Mathematics.canvas|Mathematics]] canvas. 

Each box contains one field, or topic, and they are connected to other boxes with the arrow indicating the direction from "more general" to "less general and more special". Click headings in this canvas to go to relevant sections in this note.

Of course, many more arrows could be drawn, and many more boxes could be added. In order to make the graph not too cluttered and confusing, we keep only main links.

**NOTE:** Topics marked with a ♥ are considered of prime importance to any quantum chemist, regardless of their specialization.



## Logic and Set Theory


Logic is the branch of mathematics and philosophy that deals with reasoning, the principles of valid inference, and the structure of propositions, i.e., mathematical statements. It provides the formal framework used to analyze and construct mathematical proofs, ensuring that conclusions follow from premises in a valid and systematic way.

Set theory is the branch of mathematics that studies sets, which are collections of objects. In set theory, everything is a set. It forms the foundation for much (all?) of modern mathematics, providing the language and basic concepts used to describe and analyze mathematical structures. Set theory forms the foundation in the sense that every other mathematical theory can be formalized in the language of set theory.

Most mathematicians are aware of formal set theory, but the "version" used in most contexts is "naive set theory", which in a more informal manner defines mathematical sets compared to the rigorous axiom based constructions. As Russel's Paradox shows us, naive set theory has some pitfalls. Most mathematicians simply avoid these pitfalls and stick to naive set theory.

Although formal set theory is unlikely to be applied in the study of quantum chemistry, the basic notation is widely-used and an important language tool when specifying computational methods and their implementation. 

Recommended reading:

>[!book] An Introduction to Proofs with Set Theory by Ashlock and Lee
>![[Pasted image 20240829092150.png|300]]
>Springer (2020)
>https://link.springer.com/book/10.1007/978-3-031-02426-9
>
>A in introduction to logic, set theory, and mathematical proofs for the undergraduate student. Highly recommended!
>
>A link to the set theory chapter available online: https://www.math.uh.edu/~dlabate/settheory_Ashlock.pdf

>[!book] "Set Theory for the Working Mathematician" by Krzysztof Ciesielski
> ![[Pasted image 20240829091657.png]]
> 
> A more advanced text.
> 
> Cambridge University Press (1997) https://doi.org/10.1017/CBO9781139173131



## Category Theory

Category theory is a branch of mathematics that provides a high-level, abstract framework for describing and analyzing mathematical structures and their relationships. It was developed in the 1940s by Samuel Eilenberg and Saunders Mac Lane, and has found applications across nearly all areas of mathematics, as well as in computer science, logic, and theoretical physics.

One of the useful aspects of category theory is that it gives a rigorous language for comparing different mathematical concepts and structures, such as groups and vector spaces.

Although direct use of category theory in quantum chemistry is rare, it is mentioned here as an important branch of modern mathematics.

Recommended reading:
>[!book] A Gentle Introduction to Category Theory by Maarten Fokkinga
>A set of lecture notes. Link to PDF on the author's web site:
>https://maartenfokkinga.github.io/utwente/mmf92b.pdf



## Discrete Mathematics

Lorem ipsum ...
Recommended reading:
>[!book] Concrete Mathematics by Donald Knuth
>![[Pasted image 20240829093357.png]]
>Addison-Wesley (1994)
>
>A classic textbook.
>
>https://en.wikipedia.org/wiki/Concrete_Mathematics
>https://web.archive.org/web/20201106232418/http://www-cs-faculty.stanford.edu/~knuth/gkp.html
>
>

>[!book] Introduction to Graph Theory by Douglas B. West
>![[Pasted image 20240829094014.png|300]]
>
>Link to full book (only for preview): https://daiwz.net/course/disc_math/2023/West_Intro_Graph_Theory_en.pdf
>


## Abstract Algebra

In abstract algebra, sets are given *mathematical structure* in the form of binary operations and various axioms that define what it is to be, e.g., a *group*. Thus, a group is defined in terms of its essential features, and not its concrete realizations. For example, the group $\mathbb{Z}_4 = \{0, 1, 2, 3\}$ with group operation of addition modulo 4, compared to the matrix group consisting of powers of the matrix $[[0, 1], [-1, 0]]$.

Important algebraic constructions include groups, semigroups, rings, modules, vector spaces, and algebras.

Abstract algebra is important for quantum chemistry, since it lays the foundation for linear algebra, one of the most important tools of the scientist, and the study of molecular symmetries and groups.

Recommended reading:
>[!book] A First Course in Abstract Algebra by John B. Fraleigh
>Seventh Edition, Pearson (2003)
>![[Screenshot 2024-08-29 at 09.49.31.png|300]]
>Archived book: https://archive.org/details/firstcourseinabs07edfral


## ♥ Group Theory


Group theory is the study of abstract groups and their representations. Lie groups are groups that are also differentiable manifolds (see Differential Geometry). Group theory permeates theoretical physics and chemistry, giving an axiomatic treatment of symmetry. Representation theory studies groups represented as linear operators or matrices acting on vector spaces.

In chemistry, molecular symmetries and point groups are useful for understanding molecular behavior and also eases interpretation of spectroscopic experiments. Spectroscopic notation is a consequence of conservation of angular momentum. Representation theory is applied to explain the symmetries of molecular orbitals. Having a grasp of group theory is _absolutely essential_ for the quantum chemist.

Recommended reading:

>[!book] Group Theory and Chemistry by David M. Bishop
>![[Pasted image 20240829095053.png|300]]
>Dover (1973)
>
>A classic textbook, very useful.
>
>Link to PDF for preview:  https://library.navoiy-uni.uz/files/david%20m.%20bishop%20-%20group%20theory%20and%20chemistry%20(revised%20edition)(1993)(294s).pdf
>


## Number systems

The axiomatic definition of the natural numbers using set theory is one of the simplest examples of how set theory serves as foundation for mathematics. The natural numbers are again used to define the integers, rational numbers, real numbers, and complex numbers. These sets are of course among the most important mathematical objects in the sciences. The number systems are again examples of algebraic structures: the integers form a group under addition, the real and complex numbers form fields.

Clearly, understanding numbers is essential to any scientific study. On the other hand, for most purposes, intuitive notions about integers, reals, and complex numbers will be sufficient.

Recommended reading:

* See [[#Logic and Set Theory]]



## Topology

Topology is the study of open and closed sets, and the concept of continuity. A topological space is a set together with a collection of subsets called open subsets, and axioms that these have to obey. From this, topological spaces are generated, allowing us to talk about "closeness" of elements in the set. For example, a metric is an example of a structure that gives rise to a particular kind of topology, that formalizes the notion of distance between points.

In topology the notion of sequences and their convergence is made abstract, including the notion of continuous functions. Topological arguments are indispensable for mathematical analysis of partial differential equations.

For quantum chemists, being aware of the various notions of topology is useful to navigate the literature. For example, the convergence of the pseudocontinuum of the FCI method can be formalized with topological notions. As another example, in density-functional theory, what does it mean that two electronic densities are close together? Being able to distinguish different notions of "closeness of densities" is imperative for understanding, say, modes of convergence of SCF iterations.


Recommended reading:
>[!book] Topology by James R. Munkres
>![[Munkres.png|300]]
>
>Pearson (2014)
>
>This is a classic textbook.
>
>Link to PDF (for preview): https://people.math.ethz.ch/~dkosanovic/24-FS/Munkres-Topology.pdf
>

## Measure and integration

Measure theory develops abstract notions of length, area, volume, etc., and allows to speak about such notions in potentially very abstract spaces. For example, the Dirac delta function is rigorously defined using measure theory. 

The Lebesgue integral is based on the notion of a Borel measure, and generalizes the Riemann integral. With the Lebesgue integral we can integrate many more functions compared to the Riemann integral,  and operations like exchanging limits and integrals or integration variables obey well-defined and simple theorems. The Lebesgue integral is also necessary to define the $L^2$ Hilbert space of quantum mechanics. 

A passing knowledge if measure theory is very useful for the quantum chemist, since much of the language used in mathematical physics relies on these concepts. That being said, detailed theorems are rarely used, except in borderline cases, where apparent paradoxes may arise. In those cases, these paradoxes are resolved by checking the conditions for, say, interchange of limits and integration.

Recommended reading:
>[!book] The Elements of Integration and Lebesgue Measure by Robert G. Bartle
>![[Bartle.png|300]]
>Wiley Classics, 1995
>
>A slim yet classic textbook on measure and integration.


## Distribution theory

With distribution theory one extends the concept of functions to include objects, known as _distributions_ or _generalized functions_, which can be used to rigorously define operations like differentiation even for functions that are not classically differentiable. This theory is particularly useful in handling singularities or discontinuities, such as the Dirac delta function, which models an infinitely concentrated point of mass or charge. Distribution theory provides a powerful framework for solving partial differential equations, e.g., using Green's functions.

A rudimentary knowledge of distribution theory is very useful in the study of quantum mechanics. The standard informal view is that "the Dirac delta is a function which is infinite everywhere except at a single point where it is infinity", similarly that "the Green's function is the response of the system to a Dirac delta function", is very useful, but will only take one so far.

Useful in (for example):
- Response theory
- Manybody Green's function theory
- Electromagnetism

Recommended reading:

> [!book] "Mathematical Methods in Physics" by Philippe Blanchard and Erwin Brüning
> 
> ![[Blanchard and Bruening.png|300]]

>[!book] See also the book by [[Recommended General Mathematics Reading#"Mathematical Physics" by Butkov|Butkov]]



## ♥ Linear Algebra


In linear algebra, one studies linear vector spaces and linear functions between such spaces. Typical, and indeed archetypal, examples are $\mathbb{R}^n$ and $\mathbb{C}^n$, and $n\times m$ matrices with complex or real entries. It is no exaggeration that linear algebra is perhaps the most important tool in science, being at the heart of everything from quantum mechanics, data analysis, and numerical methods for the solution of partial differential equations.

Having a good command of linear algebra is _absolutely essential_ to any theoretical chemist, from the LCAO approach to molecular orbitals, via practical realizations of Kohn--Sham density functional theory, to the numerical solution of, say, the coupled-cluster method.

Recommended reading:

> [!book]  "Linear Algebra Done Right" by Sheldon Axler
> ![[Linear Algebra Done Right.png|300]]
> 
> A highly regarded undergraduate text in linear algebra, considered a very fine piece of didacic writing. Open access. Available for free on the Author's web page: https://linear.axler.net/
> 
  

>[!book] "Introduction to Linear Algebra" by Gilbert Strang
>![[Strang.png|300]]
> A great book by one of the all time greats in linear algebra. See also the [[Recommended YouTube channels]].  
> 
> https://bookstore.ams.org/view?ProductCode=STRANG/5
> 
>

## Multilinear algebra

In multilinear algebra, linear maps between vector spaces are generalized to maps over several vector spaces to several vector spaces at once, i.e., tensors. Multilinear algebra is rarely taught together with linear algebra, but could well be a subtopic in an advanced course, especially considering it is an important part of modern machine learning methodology. Multilinear algebra finds important use cases in differential geometry, as well as appearing naturally in calculus of several variables. Tensors are also integral to manybody methods like coupled-cluster theory or configuration-interaction theort.

Multilinear algebra is among the more useful topics for quantum chemists.

Recommended reading:

>[!book] "Multilinear Algebra" by Werner Greub
>A springer book on multilinear algebra that I have seen recommended. I have no experience with this book myself.
>
>Springer Verlag.
>Weblink: https://link.springer.com/book/10.1007/978-1-4613-9425-9
>![[Greub.png|300]]


>[!book] "Multilinear Algebra and its Applications"
>Lecture notes: https://www2.math.ethz.ch/education/bachelor/lectures/fs2016/other/mla/ma.pdf 
>
>Course web page at ETH: https://www2.math.ethz.ch/education/bachelor/lectures/fs2016/other/mla.html
>
>The author's name is not disclosed, but the professor that taught the course in 2016 was [Prof. Dr. Özlem Imamoḡlu](https://people.math.ethz.ch/~oezlemi/)


## ♥ Calculus

Calculus is the branch of mathematics that studies continuous change and is divided into two main areas: differential calculus and integral calculus. Differential calculus focuses on the concept of the derivative, rates of change. Integral calculus, on the other hand, deals with the concept of the integral.

Multivariate calculus extends to functions of several variables, encompassing the study of partial derivatives, multiple integrals, and vector calculus. 

Calculus, together with linear algebra, forms the foundation for much of modern science. It is _absolutely essential_ to have a good grasp of calculus and multivariate calculus for theoretical chemists.

Recommended reading:
>[!book] Vector Calculus by Jerrold E. Marsden and Anthony Tromba
>![[Marsden_frontpage.png|300]]
>

## Complex analysis

Complex analysis studies the calculus of functions of complex variables. For complex functions, being differentiable is a much more restricting requirement than for real functions, leading to surprising and very strong results of great use in physics and chemistry. Since real functions often are special cases of complex functions, complex analysis is very useful even if complex numbers do not show up at all in a theory.

Useful in: Response theory, quantum dynamics, integral evaluation, perturbation theory, to name a few.

Complex analysis is among the more useful topics for quantum chemists.

Recommended reading:
>[!book] The book by [[Recommended General Mathematics Reading#"Mathematical Physics" by Butkov]] is useful.

>[!book] Complex Analysis by Theodore Gamelin
>![[Pasted image 20240829095847.png|300]]
>Springer (2001).
>
>A very pedagogical textbook.



## Differential Geometry

Differential geometry studies curves, surfaces, and higher-dimensional analogues from an abstract perspective, called differentiable manifolds. These are characterized by the fact that they somehow are smooth, and that locally, i.e., in for sufficiently small neighborhoods of points (if one zooms in on any point), they look like flat space, i.e., $\RR^n$ (or $\CC^n$ for complex manifolds). Thus, differential geometry combines multivariate calculus and linear algebra. One has infinite dimensional versions of the theory, as well, where the modelling spaces are infinite dimensional Banach or Hilbert spaces.

Differential geometry is very useful for abstract understanding of manybody wavefunction methods. For example, the concept of orbital invariance in CASSCF, or the manifold structure of the Hartree-Fock or coupled-cluster methods. See also lie group theory.

Differential geometry is also the foundation for general relativity, and, to a lesser extent, special relativity.

Differential geometry is among the more useful branches of mathematics for quantum chemistry students.

Recommended reading:
>[!book] Geometry of Physics by Theodore Frankel
>![[Pasted image 20240829100049.png]]
>Third Edition, Cambridge University Press (2011)
>A fantastic book.
>Weblink: https://www.cambridge.org/core/books/the-geometry-of-physics/94894F70DB22055BD7BC2B84C135ABAF?pageNum=2&searchWithinIds=94894F70DB22055BD7BC2B84C135ABAF&productType=BOOK_PART&searchWithinIds=94894F70DB22055BD7BC2B84C135ABAF&productType=BOOK_PART&sort=mtdMetadata.bookPartMeta._mtdPositionSortable%3Aasc&pageSize=30&template=cambridge-core%2Fbook%2Fcontents%2Flistings&ignoreExclusions=true

>[!book] Fundamentals of Differential Geometry by Serge Lang
>![[Pasted image 20240829100530.png|300]]
>Springer (1999)
>A classic texbook.
>https://link.springer.com/book/10.1007/978-1-4612-0541-8
>

>[!book]  Differential Geometry of Curves and Surfaces by Manfredo do Carmo
>![[Pasted image 20240829100909.png|300]]
>Prentice-Hall (1976)
>
>A gentle introduction to differential geometry, mostly sticking to familiar Euclidean space.
>
>Link to PDF (for preview): http://www2.ing.unipi.it/griff/files/dC.pdf
>
>do Carmo also has a more advanced book, "Riemannian Geometry"
>![[Pasted image 20240829101030.png|300]]
>Birkhäuser (1992)
>
>Weblink: https://link.springer.com/book/9780817634902
>
>I have used this book sometimes, and it is quite good.
>

>[!book] Manifolds, Tensor Analysis, and Applications by Ralph Abraham, Jerrold E. Marsden, and Tudor Ratiu
>![[Pasted image 20240829164212.png|300]]
>Springer (1988)
>Weblink: https://link.springer.com/book/10.1007/978-1-4612-1029-0
>Archived book: https://archive.org/details/manifoldstensora00abra_0



## Convex Analysis

Convex analysis deals with convex sets and functions. It is an important branch of mathematics, since many optimization problems in science enjoy the property of convexity. Convex analysis introduces a duality transformation, the Legendre-Fenchel transformation, which in many ways are analogous to the Fourier transform.

Convex analysis plays a prominent role in the mathematical foundation of DFT, as pioneered by E.H. Lieb. The Legendre-Fenchel transformation is also important in thermodynamics.

Convex analysis is a useful topic, especially if one wants to study DFT.

Recommended reading:
>[!book] Convex Analysis - An Introductory Text by Jan van Tiel
>![[cover.jpg|300]]
>Wiley (1984)
>
>This is a slim book but highly readable!




## Functional Analysis



Functional analysis can be viewed as infinite dimensional linear algebra. Here, complete normed spaces (Banach spaces) and complete inner product spaces (Hilbert spaces) are studied, along with linear operators between such spaces. Functional analysis is the foundation of quantum mechanics, as done by J. von Neumann. In a way, one can say that the development of functional analysis in the early 20th century was motivated by placing quantum mechanics on rigorous ground.

Functional analysis also provides the mathematical language for abstract treatment of PDEs such as the Schrödinger equation, the Kohn--Sham approach to DFT, Maxwell's equations, and so on.

Functional analysis is a very useful topic for quantum chemists, especially when you want to navigate the more mathematics heavy literature.

Recommended reading:
>[!book] Introductory Functional Analysis with Applications by Erwin Kreyszig
>
> ![[Screenshot 2024-08-29 at 10.15.24.png|300]]


## ♥ Calculus of Variations

Calculus of variations deals with the optimization of nonlinear functionals, functions that map _functions_ to scalars. Calculus of variations generalizes vector calculus to infinite dimensions, and as such could also be called "nonlinear functional analysis". Calculus of variations is the correct framework for variational formulations of the laws of nature, from quantum field theory and QED to Hamilton's equations of motion. Moreover, nonlinear approximations to the molecular Schrödinger equation such as Hartree-Fock is naturally formulated in this language.

To have a basic grasp of calculus of variations is almost essential to quantum chemists. A basic knowledge does not require advanced functional analysis, even if the above paragraph gives such an expression.

Calculus of variations is thus an exceedingly important topic in quantum chemistry.

Recommended reading:
- Goldstein, Safko and Poole, "Classical Mechanics"
- Zeidler, "Nonlinear functional analysis"
- ...


## ♥ Ordinary differential equations

Ordinary differential equations (ODEs) describe initial value and boundary value problems of scalar quantities, or coupled such equations. From classical mechanics to rate equations, ODEs permeate theoretical chemistry, and having a basic understanding of essential mathematical results is absolutely essential.

Recommended reading:
* ...

## Partial differential equations

Partial differential equations (PDEs) generalize ODEs to infinite dimensions, i.e., initial and boundary value problems where the unknown is no longer a scalar or a vector, but an element in a function space. Laws such as Einstein's gravitation theory, transport of heat, chemical reaction-diffusion systems, Maxwell's equations, the various Schrödinger equations, are all PDEs.

PDEs are very important for quantum chemistry.

Recommended reading:
>[!book] Partial Differential Equations by Lawrence C. Evans
> ![[Evans-frontpage.png|300]]
> Second Edition, American Mathematical Society (2010)
> A popular textbook in PDEs.
> Link to PDF (for preview): http://home.ustc.edu.cn/~wclw8181/wffc.files/Partial%20Differential%20Equations.Evans.pdf

>[!book] Functional Analysis, Sobolev Spaces, and Partial Differential Equations by Haim Brezis
>
> ![[Screenshot 2024-08-29 at 16.29.30.png|300]]
>Springer (2011)
> A highly readable book focusing on an abstract framework for PDEs.
> Weblink: https://link.springer.com/book/10.1007/978-0-387-70914-7
  
 

## Operator Algebra

In operator algebra, one studies algebras of operators over linear spaces, often Hilbert spaces. The algebras are often given structures inspired by quantum mechanics, such as canonical anticommutator or canonical commutator relations, e.g. the CAR and CCR algebras. It is a highly abstract branch of pure mathematics, and understanding the basic notions and results may be very useful for the study of manybody theory and quantum field theories.

Recommended reading:

>[!book] Operator Algebras and Quantum Statistical Mechanics by Ola Bratteli and Derek W. Robinson
>![[Pasted image 20240829163631.png|300]]
>Springer (1987)
>A classic textbook, but quite dense, in my opinion.
>Weblink: https://link.springer.com/book/10.1007/978-3-662-02520-8


>[!book] A Course in Operator Theory by John B. Conway
>![[Screenshot 2024-08-30 at 08.41.32.png|300]]
>American Mathematical Society (1999)
>Link: https://bookstore.ams.org/GSM/21
>"This is an excellent course in operator theory and operator algebras ... leads the reader to deep new results and modern research topics ... the author has done more than just write a good book—he has managed to reveal the unspeakable charm of the subject, which is indeed the ‘source of happiness’ for operator theorists."  - _Mathematical Reviews_

>[!book] A list of books for students studying operator algebras
>Link: https://math.vanderbilt.edu/peters10/students.html
>

- See also [[Recommended General Mathematics Reading#"Mathematical Methods in Physics" by Blanchard and Brüning]]







## Numerical analysis

Most equations in quantum chemistry cannot be solved analytically, and must be approximated in finite precision arithmetic on computers. This is the area of numerical analysis. Here, numerical methods for differential equations are studied, as well as numerical linear algebra and eigenvalue finding algorithms, to name some topics.

Numerical analysis is very important for developing and understanding computer implementations of quantum chemistry algorithms.

Recommended reading:
>[!book] Numerical Analysis by Francis B. Hildebrand
>![[Pasted image 20240830084959.png|300]]
>Dover (1956)
>Archived version: https://archive.org/details/introduction_to_numerical_analysis_hildebrand
>
> A classic textbook.

>[!book] Fundamentals of Numerical Computation by Tobin A. Driscoll and Richard J. Braun
>![[Pasted image 20240830085921.png|300]]
>SIAM
>
>A modern textbook of very high quality also available completely for free online. Python, MATLAB, and Julia versions.
>Link: https://tobydriscoll.net/book/fnc/index.html
>Complete book: https://tobydriscoll.net/fnc-julia/frontmatter.html
>


## ♥ Optimization and root finding

Optimization, really a subfield of numerical analysis, deals with finding local or global extremal points of functions of several variables, as well as finding roots of systems of nonlinear equations. There are a multitude of algorithms, such as the method of steepest descent, Newton, and quasi-Newton methods. A very important topic for students of quantum chemistry, as many computational problems end up as an optimization problem.

Recommended reading:
>[!book] Numerical Optimization by Jorge Nocedal and Stephen J. Wright
>![[Screenshot 2024-08-30 at 08.46.35.png|300]]
>Springer (2006)
>Link to PDF (for preview): https://www.math.uci.edu/~qnie/Publications/NumericalOptimization.pdf
>Link: https://link.springer.com/book/10.1007/978-0-387-40065-5
>
> This is an excellent book which I have used a lot.
> 
-
